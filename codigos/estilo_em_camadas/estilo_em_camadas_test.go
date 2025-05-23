package main

import (
	"bytes"
	"fmt"
	"io"
	"os"
	"reflect"
	"strings"
	"testing"
)

// TestMySQLRepositorioProduto tests the MySQLRepositorioProduto implementation.
func TestMySQLRepositorioProduto(t *testing.T) {
	repo := &MySQLRepositorioProduto{}
	produto1 := Produto{Nome: "Notebook", Preco: 5000}
	produto2 := Produto{Nome: "Mouse", Preco: 150}

	// Test Salvar for produto1
	oldStdout1 := os.Stdout
	rPipe1, wPipe1, _ := os.Pipe()
	os.Stdout = wPipe1

	repo.Salvar(produto1)

	wPipe1.Close()
	os.Stdout = oldStdout1
	var buf1 bytes.Buffer
	io.Copy(&buf1, rPipe1)
	rPipe1.Close()

	if !strings.Contains(buf1.String(), "Produto salvo no MySQL.") {
		t.Errorf("Expected 'Produto salvo no MySQL.' log for produto1, got '%s'", buf1.String())
	}
	if len(repo.produtos) != 1 || !reflect.DeepEqual(repo.produtos[0], produto1) {
		t.Errorf("Salvar did not add produto1 correctly. Got: %v", repo.produtos)
	}

	// Test Salvar for produto2
	oldStdout2 := os.Stdout
	rPipe2, wPipe2, _ := os.Pipe()
	os.Stdout = wPipe2

	repo.Salvar(produto2)

	wPipe2.Close()
	os.Stdout = oldStdout2
	var buf2 bytes.Buffer
	io.Copy(&buf2, rPipe2)
	rPipe2.Close()

	if !strings.Contains(buf2.String(), "Produto salvo no MySQL.") {
		t.Errorf("Expected 'Produto salvo no MySQL.' log for produto2, got '%s'", buf2.String())
	}
	if len(repo.produtos) != 2 || !reflect.DeepEqual(repo.produtos[1], produto2) {
		t.Errorf("Salvar did not add produto2 correctly. Got: %v", repo.produtos)
	}

	// Test Listar
	oldStdoutList := os.Stdout
	rList, wList, _ := os.Pipe()
	os.Stdout = wList

	listaProdutos := repo.Listar()

	wList.Close()
	os.Stdout = oldStdoutList
	var bufList bytes.Buffer
	io.Copy(&bufList, rList)
	rList.Close()

	if !strings.Contains(bufList.String(), "Listando produtos do MySQL.") {
		t.Errorf("Expected 'Listando produtos do MySQL.' log, got '%s'", bufList.String())
	}

	expectedList := []Produto{produto1, produto2}
	if !reflect.DeepEqual(listaProdutos, expectedList) {
		t.Errorf("Listar returned incorrect list. Got: %v, Want: %v", listaProdutos, expectedList)
	}
}

// TestPostgreSQLRepositorioProduto tests the PostgreSQLRepositorioProduto implementation.
func TestPostgreSQLRepositorioProduto(t *testing.T) {
	repo := &PostgreSQLRepositorioProduto{}
	produto1 := Produto{Nome: "Teclado", Preco: 300}
	produto2 := Produto{Nome: "Monitor", Preco: 1200}

	// Test Salvar for produto1
	oldStdout1 := os.Stdout
	rPipe1, wPipe1, _ := os.Pipe()
	os.Stdout = wPipe1

	repo.Salvar(produto1)

	wPipe1.Close()
	os.Stdout = oldStdout1
	var buf1 bytes.Buffer
	io.Copy(&buf1, rPipe1)
	rPipe1.Close()

	if !strings.Contains(buf1.String(), "Produto salvo no PostgreSQL.") {
		t.Errorf("Expected 'Produto salvo no PostgreSQL.' log for produto1, got '%s'", buf1.String())
	}
	if len(repo.produtos) != 1 || !reflect.DeepEqual(repo.produtos[0], produto1) {
		t.Errorf("Salvar did not add produto1 correctly. Got: %v", repo.produtos)
	}

	// Test Salvar for produto2
	oldStdout2 := os.Stdout
	rPipe2, wPipe2, _ := os.Pipe()
	os.Stdout = wPipe2

	repo.Salvar(produto2)

	wPipe2.Close()
	os.Stdout = oldStdout2
	var buf2 bytes.Buffer
	io.Copy(&buf2, rPipe2)
	rPipe2.Close()

	if !strings.Contains(buf2.String(), "Produto salvo no PostgreSQL.") {
		t.Errorf("Expected 'Produto salvo no PostgreSQL.' log for produto2, got '%s'", buf2.String())
	}
	if len(repo.produtos) != 2 || !reflect.DeepEqual(repo.produtos[1], produto2) {
		t.Errorf("Salvar did not add produto2 correctly. Got: %v", repo.produtos)
	}

	// Test Listar
	oldStdoutList := os.Stdout
	rList, wList, _ := os.Pipe()
	os.Stdout = wList

	listaProdutos := repo.Listar()

	wList.Close()
	os.Stdout = oldStdoutList
	var bufList bytes.Buffer
	io.Copy(&bufList, rList)
	rList.Close()

	if !strings.Contains(bufList.String(), "Listando produtos do PostgreSQL.") {
		t.Errorf("Expected 'Listando produtos do PostgreSQL.' log, got '%s'", bufList.String())
	}

	expectedList := []Produto{produto1, produto2}
	if !reflect.DeepEqual(listaProdutos, expectedList) {
		t.Errorf("Listar returned incorrect list. Got: %v, Want: %v", listaProdutos, expectedList)
	}
}

// MockRepositorioProduto is a mock implementation of RepositorioProduto for testing.
type MockRepositorioProduto struct {
	SalvarCalled bool
	SavedProduto Produto
	ListarCalled bool
	Produtos     []Produto // Products to be returned by Listar
}

func (m *MockRepositorioProduto) Salvar(produto Produto) {
	m.SalvarCalled = true
	m.SavedProduto = produto
	// Add to internal list to mimic real repo behavior for subsequent Listar calls in tests.
	m.Produtos = append(m.Produtos, produto)
}

func (m *MockRepositorioProduto) Listar() []Produto {
	m.ListarCalled = true
	return m.Produtos
}

// TestProdutoServico tests the ProdutoServico.
func TestProdutoServico(t *testing.T) {
	mockRepo := &MockRepositorioProduto{}
	servico := &ProdutoServico{repositorio: mockRepo}

	// Test AdicionarProduto
	nomeProduto := "Cadeira Gamer"
	precoProduto := float64(1500)

	servico.AdicionarProduto(nomeProduto, precoProduto)

	if !mockRepo.SalvarCalled {
		t.Error("Expected Salvar to be called on repository, but it was not.")
	}
	expectedProduto := Produto{Nome: nomeProduto, Preco: precoProduto}
	if !reflect.DeepEqual(mockRepo.SavedProduto, expectedProduto) {
		t.Errorf("Salvar called with incorrect product. Got: %v, Want: %v", mockRepo.SavedProduto, expectedProduto)
	}
	// Verify that the product was added to the mock repo's internal list
	if len(mockRepo.Produtos) != 1 || !reflect.DeepEqual(mockRepo.Produtos[0], expectedProduto) {
		t.Errorf("Product not added to mock repo's internal list. Got: %v", mockRepo.Produtos)
	}


	// Test ExibirProdutos
	// Reset SalvarCalled, SavedProduto from previous part of the test.
	mockRepo.SalvarCalled = false
	mockRepo.SavedProduto = Produto{}

	// Set a specific list for ExibirProdutos to ensure it uses what Listar provides.
	// This overwrites mockRepo.Produtos for testing ExibirProdutos with a controlled dataset.
	mockRepo.ListarCalled = false
	produtosParaListar := []Produto{
		{Nome: "Produto Teste A", Preco: 10.99},
		{Nome: "Produto Teste B", Preco: 20.50},
	}
	mockRepo.Produtos = produtosParaListar // Set exactly what Listar should return

	oldStdout := os.Stdout
	rPipe, wPipe, _ := os.Pipe()
	os.Stdout = wPipe

	servico.ExibirProdutos()

	wPipe.Close()
	os.Stdout = oldStdout

	var buf bytes.Buffer
	io.Copy(&buf, rPipe)
	rPipe.Close()

	if !mockRepo.ListarCalled {
		t.Error("Expected Listar to be called on repository, but it was not.")
	}

	output := buf.String()
	expectedOutputA := fmt.Sprintf("Produto: %s, Preço: R$%.2f", produtosParaListar[0].Nome, produtosParaListar[0].Preco)
	expectedOutputB := fmt.Sprintf("Produto: %s, Preço: R$%.2f", produtosParaListar[1].Nome, produtosParaListar[1].Preco)

	if !strings.Contains(output, expectedOutputA) {
		t.Errorf("ExibirProdutos output missing for Produto A. Expected to contain '%s', Got: '%s'", expectedOutputA, output)
	}
	if !strings.Contains(output, expectedOutputB) {
		t.Errorf("ExibirProdutos output missing for Produto B. Expected to contain '%s', Got: '%s'", expectedOutputB, output)
	}
}
