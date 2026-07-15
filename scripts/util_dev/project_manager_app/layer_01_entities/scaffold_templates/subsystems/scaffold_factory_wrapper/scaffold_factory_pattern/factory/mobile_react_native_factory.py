class MobileReactNativeFactory:
    """
    Concrete Factory tạo các UI templates cho Mobile React Native (TypeScript/TSX).
    """

    def create_page(self, pascal_name: str, snake_name: str) -> str:
        return f"""
import React from 'react';
import {{ StyleSheet, Text, View, TouchableOpacity }} from 'react-native';
import {{ use{pascal_name} }} from '../hooks/use_{snake_name}';

export const {pascal_name}Screen: React.FC = () => {{
  const hook = use{pascal_name}();

  return (
    <View style={{styles.container}}>
      <Text style={{styles.title}}>{pascal_name} Feature</Text>
      <Text style={{styles.subtitle}}>
        This is a Clean Architecture feature scaffolded dynamically for React Native.
      </Text>
      <TouchableOpacity 
        style={{styles.button}}
        onPress={{() => {{ /* trigger logic */ }}}}
      >
        <Text style={{styles.buttonText}}>Execute Feature Action</Text>
      </TouchableOpacity>
    </View>
  );
}};

const styles = StyleSheet.create({{
  container: {{
    flex: 1,
    backgroundColor: '{{ DARK_BG }}', // Theme Background
    padding: 16,
    justifyContent: 'center',
    alignItems: 'center',
  }},
  title: {{
    fontSize: 24,
    color: '{{ TEXT_COLOR }}',
    fontWeight: 'bold',
    marginBottom: 8,
  }},
  subtitle: {{
    fontSize: 16,
    color: '{{ SUBTEXT_COLOR }}',
    textAlign: 'center',
    marginBottom: 20,
  }},
  button: {{
    backgroundColor: '{{ ACCENT_COLOR }}',
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: {{ RADIUS_NUM }},
  }},
  buttonText: {{
    color: '{{ DARK_BG }}',
    fontWeight: 'bold',
    fontSize: 16,
  }},
}});
"""

    def create_buttons(self) -> str:
        return """
import React from 'react';
import { StyleSheet, Text, TouchableOpacity } from 'react-native';

interface ButtonProps {
  text: string;
  onPressed: () => void;
  color?: string;
}

export const AtomButton: React.FC<ButtonProps> = ({ text, onPressed, color = '{{ ACCENT_COLOR }}' }) => {
  return (
    <TouchableOpacity style={[styles.button, { backgroundColor: color }]} onPress={onPressed}>
      <Text style={styles.text}>{text}</Text>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  button: {
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderRadius: {{ RADIUS_NUM }},
    alignItems: 'center',
  },
  text: {
    color: '{{ DARK_BG }}',
    fontWeight: 'bold',
  },
});
"""

    def create_inputs(self) -> str:
        return """
import React from 'react';
import { StyleSheet, TextInput } from 'react-native';

interface InputProps {
  hintText: string;
  value: string;
  onChangeText: (text: string) => void;
  obscureText?: boolean;
}

export const AtomInput: React.FC<InputProps> = ({ hintText, value, onChangeText, obscureText = false }) => {
  return (
    <TextInput
      placeholder={hintText}
      placeholderTextColor="{{ SUBTEXT_COLOR }}"
      value={value}
      onChangeText={onChangeText}
      secureTextEntry={obscureText}
      style={styles.input}
    />
  );
};

const styles = StyleSheet.create({
  input: {
    backgroundColor: '{{ CARD_BG }}',
    color: '{{ TEXT_COLOR }}',
    padding: 12,
    borderRadius: {{ RADIUS_NUM }},
    fontSize: 16,
  },
});
"""

    def create_labels(self) -> str:
        return """
import React from 'react';
import { StyleSheet, Text } from 'react-native';

interface LabelProps {
  text: string;
  fontSize?: number;
  bold?: boolean;
  color?: string;
}

export const AtomLabel: React.FC<LabelProps> = ({ text, fontSize = 16, bold = false, color = '{{ TEXT_COLOR }}' }) => {
  return (
    <Text style={{ fontSize, fontWeight: bold ? 'bold' : 'normal', color }}>
      {text}
    </Text>
  );
};
"""

    def create_async_hook(self) -> str:
        return """
import { useState } from 'react';

export const useAsync = () => {
  const [loading, setLoading] = useState(false);

  const execute = async <T>(asyncFn: () => Promise<T>, onError?: (err: string) => void): Promise<T | null> => {
    if (loading) return null;
    setLoading(true);
    try {
      return await asyncFn();
    } catch (err: any) {
      if (onError) onError(err.message || String(err));
      return null;
    } finally {
      setLoading(false);
    }
  };

  return { loading, execute };
};
"""

    def create_feature_hook(self, pascal_name: str, snake_name: str) -> str:
        return f"""
import {{ useState }} from 'react';

export const use{pascal_name} = () => {{
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  return {{ loading, errorMsg }};
}};
"""

    def create_ui_inspector(self) -> str:
        return """
import React from 'react';
import { StyleSheet, Text, View } from 'react-native';

export const UIInspector: React.FC = () => {
  return (
    <View style={styles.container}>
      <Text style={styles.text}>UI Inspector (F11 to Capture)</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 8,
    backgroundColor: 'rgba(0,0,0,0.8)',
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
  },
  text: {
    color: '#white',
    fontSize: 10,
    textAlign: 'center',
  },
});
"""

    def create_main_window(self, project_name: str) -> str:
        return f"""
import React from 'react';
import {{ SafeAreaView, StatusBar, StyleSheet }} from 'react-native';
import {{ WelcomeScreen }} from './level_05_pages/WelcomeScreen';

const App = () => {{
  return (
    <SafeAreaView style={{styles.safeArea}}>
      <StatusBar barStyle="light-content" backgroundColor="{{ DARK_BG }}" />
      <WelcomeScreen />
    </SafeAreaView>
  );
}};

const styles = StyleSheet.create({{
  safeArea: {{
    flex: 1,
    backgroundColor: '{{ DARK_BG }}',
  }},
}});

export default App;
"""
