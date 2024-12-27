## API Gateway com Microserviços em TypeScript

Este é um exemplo de um **API Gateway** minimalista em TypeScript, com suporte para redirecionamento de requisições para dois microserviços: **Clientes** e **Produtos**. 

### Comentários

- **Gateway**: Atua como intermediário entre o cliente e os microserviços, redirecionando requisições e consolidando logs.
- **Microserviços**: Ambos os serviços (Clientes e Produtos) possuem rotas simples para demonstração. 
- **Expansão**: Este modelo pode ser estendido para incluir autenticação, monitoramento, e balanceamento de carga, que são comuns em gateways de APIs


---

### Serviço de Clientes

```typescript
import express from 'express';

const clienteService = express();
clienteService.use(express.json());
const CLIENTE_PORT = 4001;

clienteService.get('/clientes', (req, res) => {
    res.send([
        { id: 1, nome: 'João Silva' },
        { id: 2, nome: 'Maria Oliveira' }
    ]);
});

clienteService.listen(CLIENTE_PORT, () => {
    console.log(`Microserviço de Clientes rodando na porta ${CLIENTE_PORT}`);
});
```

### Serviço de Produtos

```typescript
import express from 'express';

const produtoService = express();
produtoService.use(express.json());
const PRODUTO_PORT = 4002;

produtoService.get('/produtos', (req, res) => {
    res.send([
        { id: 1, nome: 'Produto A' },
        { id: 2, nome: 'Produto B' }
    ]);
});

produtoService.listen(PRODUTO_PORT, () => {
    console.log(`Microserviço de Produtos rodando na porta ${PRODUTO_PORT}`);
});
```

---

---

### Gateway de API

```typescript
// Importando os módulos necessários
import express, { Request, Response } from 'express';
import morgan from 'morgan';
import axios from 'axios';

// Inicializa o servidor Express
const app = express();
const PORT = 3000; // Porta onde o Gateway vai operar

// Middleware de logging usando Morgan
app.use(morgan('combined'));
app.use(express.json()); // Para lidar com corpos de requisições em JSON

// Rota principal do Gateway
app.use('/api/:service/*', async (req: Request, res: Response) => {
    const { service } = req.params;
    const targetUrl = resolveServiceUrl(service);

    if (!targetUrl) {
        res.status(404).send({ error: `Serviço '${service}' não encontrado no Gateway.` });
        return;
    }

    try {
        // Redireciona a requisição para o microserviço de destino
        const response = await axios({
            method: req.method,
            url: `${targetUrl}${req.originalUrl.replace(`/api/${service}`, '')}`,
            data: req.body,
            headers: req.headers
        });

        // Retorna a resposta do microserviço ao cliente
        res.status(response.status).send(response.data);
    } catch (error) {
        console.error(`Erro ao acessar o serviço '${service}':`, error);
        res.status(500).send({ error: 'Erro interno ao processar a requisição.' });
    }
});

// Função para resolver URLs dos serviços com base no nome
const resolveServiceUrl = (service: string): string | undefined => {
    const services: Record<string, string> = {
        cliente: 'http://localhost:4001', // Microserviço de clientes
        produto: 'http://localhost:4002'  // Microserviço de produtos
    };

    return services[service];
};

// Inicializa o servidor do Gateway
app.listen(PORT, () => {
    console.log(`API Gateway em execução na porta ${PORT}`);
});
```


