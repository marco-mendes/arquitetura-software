package main

import (
	"bytes"
	"io"
	"os"
	"reflect"
	"strings"
	"testing"
)

// TestUppercasePlugin tests the UppercasePlugin.
func TestUppercasePlugin(t *testing.T) {
	plugin := UppercasePlugin{}
	testCases := []struct {
		name     string
		input    string
		expected string
	}{
		{"empty string", "", ""},
		{"lowercase", "hello", "HELLO"},
		{"mixed case", "HeLlO", "HELLO"},
		{"already uppercase", "WORLD", "WORLD"},
		{"with numbers", "h3llo w0rld", "H3LLO W0RLD"},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			// Capture stdout to check log message
			oldStdout := os.Stdout
			rPipe, wPipe, _ := os.Pipe()
			os.Stdout = wPipe

			result := plugin.Run(tc.input)

			wPipe.Close()
			os.Stdout = oldStdout
			var buf bytes.Buffer
			io.Copy(&buf, rPipe)
			rPipe.Close()

			if !strings.Contains(buf.String(), "Plugin: Convertendo texto para maiúsculas.") {
				t.Errorf("Expected log message 'Plugin: Convertendo texto para maiúsculas.', got '%s'", buf.String())
			}
			if result != tc.expected {
				t.Errorf("Expected Run(%s) to be %s, got %s", tc.input, tc.expected, result)
			}
		})
	}
}

// TestReversePlugin tests the ReversePlugin.
// This also indirectly tests the unexported reverseString function.
func TestReversePlugin(t *testing.T) {
	plugin := ReversePlugin{}
	testCases := []struct {
		name     string
		input    string
		expected string
	}{
		{"empty string", "", ""},
		{"single character", "a", "a"},
		{"even length", "abcd", "dcba"},
		{"odd length", "abcde", "edcba"},
		{"palindrome", "madam", "madam"},
		{"with spaces", "hello world", "dlrow olleh"},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			// Capture stdout to check log message
			oldStdout := os.Stdout
			rPipe, wPipe, _ := os.Pipe()
			os.Stdout = wPipe

			result := plugin.Run(tc.input)

			wPipe.Close()
			os.Stdout = oldStdout
			var buf bytes.Buffer
			io.Copy(&buf, rPipe)
			rPipe.Close()
			
			if !strings.Contains(buf.String(), "Plugin: Revertendo texto.") {
				t.Errorf("Expected log message 'Plugin: Revertendo texto.', got '%s'", buf.String())
			}
			if result != tc.expected {
				t.Errorf("Expected Run(%s) to be %s, got %s", tc.input, tc.expected, result)
			}
		})
	}
}

// TestCoreSystem_RegisterPlugin tests the plugin registration functionality.
func TestCoreSystem_RegisterPlugin(t *testing.T) {
	core := CoreSystem{} // NewCoreSystem() isn't defined; CoreSystem is initialized directly.
	pluginA := UppercasePlugin{}
	pluginB := ReversePlugin{}

	if len(core.plugins) != 0 {
		t.Fatalf("Expected new CoreSystem to have 0 plugins, got %d", len(core.plugins))
	}

	core.RegisterPlugin(pluginA)
	if len(core.plugins) != 1 {
		t.Errorf("Expected 1 plugin after registering pluginA, got %d", len(core.plugins))
	}
	// Check if the registered plugin is indeed pluginA
	// This requires type assertion or a way to identify the plugin if they were more complex.
	// For this simple case, checking the type is sufficient.
	if _, ok := core.plugins[0].(UppercasePlugin); !ok {
		t.Errorf("Expected registered plugin to be UppercasePlugin, but it was not.")
	}


	core.RegisterPlugin(pluginB)
	if len(core.plugins) != 2 {
		t.Errorf("Expected 2 plugins after registering pluginB, got %d", len(core.plugins))
	}
	if _, ok := core.plugins[1].(ReversePlugin); !ok {
		t.Errorf("Expected second registered plugin to be ReversePlugin, but it was not.")
	}
}

// TestCoreSystem_Execute tests the Execute method of CoreSystem.
func TestCoreSystem_Execute(t *testing.T) {
	core := CoreSystem{}
	uppercasePlugin := UppercasePlugin{}
	reversePlugin := ReversePlugin{}

	t.Run("NoPlugins", func(t *testing.T) {
		input := "TestData"
		expected := "TestData"
		result := core.Execute(input)
		if result != expected {
			t.Errorf("Execute with no plugins: expected '%s', got '%s'", expected, result)
		}
	})

	core.RegisterPlugin(uppercasePlugin)
	t.Run("OnePlugin_Uppercase", func(t *testing.T) {
		input := "lowercase"
		expected := "LOWERCASE"
		result := core.Execute(input)
		if result != expected {
			t.Errorf("Execute with UppercasePlugin: expected '%s', got '%s'", expected, result)
		}
	})

	// Reset core for the next test case or create a new one
	core = CoreSystem{} // Resetting core
	core.RegisterPlugin(reversePlugin)
	t.Run("OnePlugin_Reverse", func(t *testing.T) {
		input := "forward"
		expected := "drawrof"
		result := core.Execute(input)
		if result != expected {
			t.Errorf("Execute with ReversePlugin: expected '%s', got '%s'", expected, result)
		}
	})
	
	// Reset core and register in a specific order
	core = CoreSystem{} // Resetting core
	core.RegisterPlugin(uppercasePlugin)
	core.RegisterPlugin(reversePlugin)
	t.Run("TwoPlugins_UppercaseThenReverse", func(t *testing.T) {
		input := "Hello" // Uppercase -> HELLO, Reverse -> OLLEH
		expected := "OLLEH"
		
		// Capture stdout to check log messages from CoreSystem and Plugins
		oldStdout := os.Stdout
		rPipe, wPipe, _ := os.Pipe()
		os.Stdout = wPipe

		result := core.Execute(input)
		
		wPipe.Close()
		os.Stdout = oldStdout
		var buf bytes.Buffer
		io.Copy(&buf, rPipe)
		rPipe.Close()
		output := buf.String()

		if result != expected {
			t.Errorf("Execute with Uppercase then Reverse: expected '%s', got '%s'", expected, result)
		}
		if !strings.Contains(output, "Core System: Processando dados iniciais.") {
			t.Error("CoreSystem Execute log 'Processando dados iniciais' missing.")
		}
		if !strings.Contains(output, "Plugin: Convertendo texto para maiúsculas.") {
			t.Error("UppercasePlugin Run log missing during combined execution.")
		}
		if !strings.Contains(output, "Plugin: Revertendo texto.") {
			t.Error("ReversePlugin Run log missing during combined execution.")
		}
		if !strings.Contains(output, "Core System: Dados finais processados.") {
			t.Error("CoreSystem Execute log 'Dados finais processados' missing.")
		}
	})

	// Test order: Reverse then Uppercase
	core = CoreSystem{} // Resetting core
	core.RegisterPlugin(reversePlugin)
	core.RegisterPlugin(uppercasePlugin)
	t.Run("TwoPlugins_ReverseThenUppercase", func(t *testing.T) {
		input := "World" // Reverse -> dlroW, Uppercase -> DLROW
		expected := "DLROW"
		result := core.Execute(input)
		if result != expected {
			t.Errorf("Execute with Reverse then Uppercase: expected '%s', got '%s'", expected, result)
		}
	})
}

// MockPlugin for testing purposes if more complex interactions are needed.
type MockPlugin struct {
	RunFunc      func(data string) string
	RunCalled    bool
	RunDataInput string
}

func (m *MockPlugin) Run(data string) string {
	m.RunCalled = true
	m.RunDataInput = data
	if m.RunFunc != nil {
		return m.RunFunc(data)
	}
	return "mocked_data_" + data // Default mock behavior
}

// TestCoreSystem_Execute_WithMockPlugin demonstrates using a mock plugin.
func TestCoreSystem_Execute_WithMockPlugin(t *testing.T) {
	core := CoreSystem{}
	mockP := &MockPlugin{
		RunFunc: func(data string) string {
			return "mock_processed_" + data
		},
	}
	core.RegisterPlugin(mockP)

	inputData := "test_input"
	expectedResult := "mock_processed_test_input"
	result := core.Execute(inputData)

	if !mockP.RunCalled {
		t.Error("MockPlugin's Run method was not called.")
	}
	if mockP.RunDataInput != inputData {
		t.Errorf("MockPlugin's Run method called with wrong data: got '%s', want '%s'", mockP.RunDataInput, inputData)
	}
	if result != expectedResult {
		t.Errorf("CoreSystem Execute with MockPlugin: expected '%s', got '%s'", expectedResult, result)
	}
}

// Helper function to compare plugin slices (if needed for more complex scenarios)
// For current tests, checking length and type assertion is sufficient.
func comparePluginSlices(a, b []Plugin) bool {
	if len(a) != len(b) {
		return false
	}
	for i := range a {
		// This comparison is tricky because plugins are interfaces.
		// reflect.TypeOf might be one way, or adding a GetName() to Plugin interface.
		if reflect.TypeOf(a[i]) != reflect.TypeOf(b[i]) {
			return false
		}
	}
	return true
}
