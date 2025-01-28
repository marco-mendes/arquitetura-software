package main

import (
	"log"
	"net"
	"net/http"
	"sync"
	"sync/atomic"
	"time"
)

// ------------------------------------------
// Estruturas principais do Chassis
// ------------------------------------------

type Config struct {
	Ambiente    string
	NomeServico string
	NivelLog    string
	APIKey      string
	LimiteRPS   int
	MaxFalhasCB int
}

type Metrics struct {
	Requisicoes   int64
	Erros         int64
	LatenciaTotal time.Duration
}

type RateLimiter struct {
	mu        sync.Mutex
	contador  map[string]int
	limite    int
	intervalo time.Duration
}

type CircuitBreaker struct {
	mu          sync.Mutex
	falhas      int
	maxFalhas   int
	estado      string
	ultimoReset time.Time
}

type Chassis struct {
	Conf           *Config
	Logger         *log.Logger
	Metricas       *Metrics
	RateLimiter    *RateLimiter
	CircuitBreaker *CircuitBreaker
}

// ------------------------------------------
// Implementação dos serviços
// ------------------------------------------

type ServicoOla struct {
	*Chassis
}

func (s *ServicoOla) HandlerOla(w http.ResponseWriter, r *http.Request) {
	// Simular erro com query parameter
	if r.URL.Query().Get("erro") == "true" {
		panic("erro simulado")
	}

	nome := r.URL.Query().Get("nome")
	s.Logger.Printf("Processando pedido para: %s", nome)
	w.Write([]byte("Olá, " + nome + "!"))
}

type ServicoSaude struct {
	*Chassis
}

func (s *ServicoSaude) HandlerSaude(w http.ResponseWriter, r *http.Request) {
	s.Logger.Printf("Verificação de saúde")
	w.Write([]byte("Saudável"))
}

// ------------------------------------------
// Implementação dos Cross-Cutting Concerns
// ------------------------------------------

func (c *Chassis) Logging(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()
		c.Logger.Printf("Início: %s %s", r.Method, r.URL.Path)

		defer func() {
			c.Logger.Printf("Fim: %s %s (%v)", r.Method, r.URL.Path, time.Since(start))
		}()

		next.ServeHTTP(w, r)
	})
}

func (c *Chassis) MetricasMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()
		atomic.AddInt64(&c.Metricas.Requisicoes, 1)

		defer func() {
			// Convert time.Duration to int64 nanoseconds before adding
			latencyNanos := time.Since(start).Nanoseconds()
			atomic.AddInt64((*int64)(&c.Metricas.LatenciaTotal), latencyNanos)
		}()

		next.ServeHTTP(w, r)
	})
}

func (c *Chassis) ValidacaoParametros(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		c.Logger.Printf("⭐ [Middleware Validação] Iniciando validação de parâmetros")
		if r.URL.Path == "/ola" && r.URL.Query().Get("nome") == "" {
			c.Logger.Printf("❌ [Middleware Validação] Parâmetro 'nome' ausente")
			http.Error(w, "Parâmetro 'nome' obrigatório", http.StatusBadRequest)
			return
		}
		c.Logger.Printf("✅ [Middleware Validação] Parâmetros válidos")
		next.ServeHTTP(w, r)
	})
}

func (c *Chassis) Autenticacao(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		c.Logger.Printf("⭐ [Middleware Auth] Verificando autenticação")
		if r.URL.Path == "/saude" {
			c.Logger.Printf("✅ [Middleware Auth] Endpoint de saúde, pulando autenticação")
			next.ServeHTTP(w, r)
			return
		}

		apiKey := r.Header.Get("X-API-Key")
		if apiKey != c.Conf.APIKey {
			c.Logger.Printf("❌ [Middleware Auth] Autenticação falhou")
			http.Error(w, "Não autorizado", http.StatusUnauthorized)
			return
		}
		c.Logger.Printf("✅ [Middleware Auth] Autenticação bem-sucedida")
		next.ServeHTTP(w, r)
	})
}

func (c *Chassis) Limitador(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		c.Logger.Printf("⭐ [Rate Limiter] Verificando limites de taxa")
		c.RateLimiter.mu.Lock()
		defer c.RateLimiter.mu.Unlock()

		// Extract only the IP address without the port
		clientIP := r.RemoteAddr
		// Add "net" package to imports at the top of the file
		// Import "net" package at the top of the file first
		if host, _, err := net.SplitHostPort(clientIP); err == nil {
			clientIP = host
		}

		if c.RateLimiter.contador[clientIP] >= c.RateLimiter.limite {
			c.Logger.Printf("❌ [Rate Limiter] Limite excedido para %s (atual: %d, limite: %d)",
				clientIP, c.RateLimiter.contador[clientIP], c.RateLimiter.limite)
			http.Error(w, "Limite de taxa excedido", http.StatusTooManyRequests)
			return
		}

		c.RateLimiter.contador[clientIP]++
		c.Logger.Printf("✅ [Rate Limiter] Requisição permitida para %s (contador: %d/%d)",
			clientIP, c.RateLimiter.contador[clientIP], c.RateLimiter.limite)

		go func() {
			time.Sleep(c.RateLimiter.intervalo)
			c.RateLimiter.mu.Lock()
			c.RateLimiter.contador[clientIP]--
			c.Logger.Printf("ℹ️ [Rate Limiter] Decrementando contador para %s (novo valor: %d)",
				clientIP, c.RateLimiter.contador[clientIP])
			c.RateLimiter.mu.Unlock()
		}()

		next.ServeHTTP(w, r)
	})
}

func (c *Chassis) CircuitBreakerMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		c.Logger.Printf("⭐ [Circuit Breaker] Verificando estado do circuito")
		c.CircuitBreaker.mu.Lock()
		if c.CircuitBreaker.estado == "open" {
			c.Logger.Printf("❌ [Circuit Breaker] Circuito aberto, rejeitando requisição")
			c.CircuitBreaker.mu.Unlock()
			http.Error(w, "Serviço indisponível", http.StatusServiceUnavailable)
			return
		}
		c.CircuitBreaker.mu.Unlock()
		c.Logger.Printf("✅ [Circuit Breaker] Circuito fechado, permitindo requisição")
		next.ServeHTTP(w, r)
	})
}

func (c *Chassis) Recuperacao(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		c.Logger.Printf("⭐ [Recovery] Iniciando middleware de recuperação")
		defer func() {
			if err := recover(); err != nil {
				atomic.AddInt64(&c.Metricas.Erros, 1)
				c.Logger.Printf("❌ [Recovery] Panic capturado: %v", err)

				c.CircuitBreaker.mu.Lock()
				c.CircuitBreaker.falhas++
				c.Logger.Printf("⚠️ [Recovery] Incrementando falhas do Circuit Breaker: %d/%d",
					c.CircuitBreaker.falhas, c.CircuitBreaker.maxFalhas)

				if c.CircuitBreaker.falhas >= c.CircuitBreaker.maxFalhas {
					c.CircuitBreaker.estado = "open"
					c.CircuitBreaker.ultimoReset = time.Now()
					c.Logger.Printf("🔴 [Recovery] Circuit Breaker aberto")
					go func() {
						time.Sleep(10 * time.Second)
						c.CircuitBreaker.mu.Lock()
						c.CircuitBreaker.estado = "half-open"
						c.CircuitBreaker.falhas = 0
						c.Logger.Printf("🟡 [Recovery] Circuit Breaker em half-open")
						c.CircuitBreaker.mu.Unlock()
					}()
				}
				c.CircuitBreaker.mu.Unlock()

				http.Error(w, "Erro interno", http.StatusInternalServerError)
			}
		}()
		next.ServeHTTP(w, r)
	})
}

// ------------------------------------------
// Inicialização e configuração
// ------------------------------------------

func NewChassis() *Chassis {
	conf := &Config{
		Ambiente:    "prod",
		NomeServico: "servico-completo",
		NivelLog:    "debug",
		APIKey:      "chave-secreta-123",
		LimiteRPS:   5,
		MaxFalhasCB: 3,
	}

	return &Chassis{
		Conf:     conf,
		Logger:   log.Default(),
		Metricas: &Metrics{},
		RateLimiter: &RateLimiter{
			contador:  make(map[string]int),
			limite:    conf.LimiteRPS,
			intervalo: time.Second,
		},
		CircuitBreaker: &CircuitBreaker{
			maxFalhas: conf.MaxFalhasCB,
			estado:    "closed",
		},
	}
}

// ------------------------------------------
// Ponto de entrada principal
// ------------------------------------------

func main() {
	chassis := NewChassis()

	// Registrar serviços
	ola := &ServicoOla{Chassis: chassis}
	saude := &ServicoSaude{Chassis: chassis}

	// Construir cadeia de middlewares na ordem correta
	handler := http.HandlerFunc(ola.HandlerOla)

	// Aplicar middlewares na ordem correta
	handler = http.HandlerFunc(chassis.ValidacaoParametros(handler).ServeHTTP)
	handler = http.HandlerFunc(chassis.Autenticacao(handler).ServeHTTP)
	handler = http.HandlerFunc(chassis.Limitador(handler).ServeHTTP)
	handler = http.HandlerFunc(chassis.MetricasMiddleware(handler).ServeHTTP)
	handler = http.HandlerFunc(chassis.Logging(handler).ServeHTTP)
	handler = http.HandlerFunc(chassis.CircuitBreakerMiddleware(handler).ServeHTTP)
	handler = http.HandlerFunc(chassis.Recuperacao(handler).ServeHTTP)

	// Configurar endpoint
	http.Handle("/ola", handler)

	// Handler de saúde sem autenticação
	http.Handle("/saude", chassis.Logging(
		chassis.Recuperacao(
			http.HandlerFunc(saude.HandlerSaude),
		),
	))

	// Iniciar servidor
	chassis.Logger.Printf("Serviço %s iniciado na porta 8080", chassis.Conf.NomeServico)
	chassis.Logger.Fatal(http.ListenAndServe(":8080", nil))
}
