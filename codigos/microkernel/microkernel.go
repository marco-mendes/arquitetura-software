package main

import (
	"fmt"
	"strings"
)

// Plugin é uma interface que define o método Run
// Padrão de Projeto: Strategy
// A interface Plugin permite que diferentes implementações de plugins sejam usadas de forma intercambiável
type Plugin interface {
	Run(data string) string
}

// CoreSystem é o núcleo do sistema que gerencia e executa plugins
// Padrão de Projeto: Microkernel
// O CoreSystem atua como o núcleo que gerencia a execução de plugins
type CoreSystem struct {
	plugins []Plugin
}

// RegisterPlugin registra um plugin no núcleo
func (c *CoreSystem) RegisterPlugin(plugin Plugin) {
	c.plugins = append(c.plugins, plugin)
}

// Execute processa os dados usando os plugins registrados
func (c *CoreSystem) Execute(data string) string {
	fmt.Println("Core System: Processando dados iniciais.")
	for _, plugin := range c.plugins {
		data = plugin.Run(data)
	}
	fmt.Println("Core System: Dados finais processados.")
	return data
}

// UppercasePlugin é um plugin que converte texto para maiúsculas
type UppercasePlugin struct{}

// Run executa a lógica do plugin UppercasePlugin
func (u UppercasePlugin) Run(data string) string {
	fmt.Println("Plugin: Convertendo texto para maiúsculas.")
	return strings.ToUpper(data)
}

// ReversePlugin é um plugin que reverte o texto
type ReversePlugin struct{}

// Run executa a lógica do plugin ReversePlugin
func (r ReversePlugin) Run(data string) string {
	fmt.Println("Plugin: Revertendo texto.")
	return reverseString(data)
}

// Função auxiliar para reverter uma string
func reverseString(s string) string {
	runes := []rune(s)
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return string(runes)
}

func main() {
	core := CoreSystem{}

	// Registra os plugins no núcleo
	core.RegisterPlugin(UppercasePlugin{})
	core.RegisterPlugin(ReversePlugin{})

	// Executa o núcleo com os plugins
	resultado := core.Execute("ALO MUNDO")
	fmt.Println("Resultado final:", resultado)
}
