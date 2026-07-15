class MobileJetpackComposeFactory:
    """
    Concrete Factory tạo các UI templates cho Mobile Jetpack Compose (Android - Kotlin).
    """

    def create_page(self, pascal_name: str, snake_name: str) -> str:
        return f"""
package com.cleanarch.app.level_05_pages

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun {pascal_name}Screen() {{
    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color({{ DARK_BG_ARGB }})) // Theme Background
            .padding(16.dp),
        contentAlignment = Alignment.Center
    ) {{
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {{
            Text(
                text = "{pascal_name} Feature",
                color = Color({{ TEXT_COLOR_ARGB }}),
                fontSize = 24.sp,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                text = "This is a Clean Architecture feature scaffolded dynamically for Jetpack Compose.",
                color = Color({{ SUBTEXT_COLOR_ARGB }}),
                fontSize = 16.sp,
                modifier = Modifier.padding(horizontal = 16.dp)
            )
            Spacer(modifier = Modifier.height(20.dp))
            Button(
                onClick = {{ /* trigger action */ }},
                colors = ButtonDefaults.buttonColors(containerColor = Color({{ ACCENT_COLOR_ARGB }}))
            ) {{
                Text(text = "Execute Feature Action", color = Color({{ DARK_BG_ARGB }}))
            }}
        }}
    }}
}}
"""

    def create_buttons(self) -> str:
        return """
package com.cleanarch.app.level_01_atoms

import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp

@Composable
fun AtomButton(
    text: String,
    onPressed: () -> Unit,
    color: Color = Color({{ ACCENT_COLOR_ARGB }})
) {
    Button(
        onClick = onPressed,
        colors = ButtonDefaults.buttonColors(containerColor = color),
        shape = RoundedCornerShape({{ RADIUS_NUM }}.dp)
    ) {
        Text(text = text, color = Color({{ DARK_BG_ARGB }}), fontWeight = FontWeight.Bold)
    }
}
"""

    def create_inputs(self) -> str:
        return """
package com.cleanarch.app.level_01_atoms

import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.TextField
import androidx.compose.material3.TextFieldDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.unit.dp

@Composable
fun AtomInput(
    value: String,
    onValueChange: (String) -> Unit,
    hintText: String,
    obscureText: Boolean = false
) {
    TextField(
        value = value,
        onValueChange = onValueChange,
        placeholder = { Text(text = hintText, color = Color({{ SUBTEXT_COLOR_ARGB }})) },
        visualTransformation = if (obscureText) PasswordVisualTransformation() else VisualTransformation.None,
        shape = RoundedCornerShape({{ RADIUS_NUM }}.dp),
        colors = TextFieldDefaults.colors(
            focusedTextColor = Color({{ TEXT_COLOR_ARGB }}),
            unfocusedTextColor = Color({{ TEXT_COLOR_ARGB }}),
            focusedContainerColor = Color({{ CARD_BG_ARGB }}),
            unfocusedContainerColor = Color({{ CARD_BG_ARGB }}),
            focusedIndicatorColor = Color.Transparent,
            unfocusedIndicatorColor = Color.Transparent
        )
    )
}
"""

    def create_labels(self) -> str:
        return """
package com.cleanarch.app.level_01_atoms

import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp

@Composable
fun AtomLabel(
    text: String,
    fontSize: Double = 16.0,
    bold: Boolean = false,
    color: Color = Color({{ TEXT_COLOR_ARGB }})
) {
    Text(
        text = text,
        fontSize = fontSize.sp,
        fontWeight = if (bold) FontWeight.Bold else FontWeight.Normal,
        color = color
    )
}
"""

    def create_async_hook(self) -> str:
        return """
package com.cleanarch.app.hooks

import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.launch

class UseAsync(private val scope: CoroutineScope) {
    var loading = false

    fun execute(asyncFn: suspend () -> Unit, onError: (String) -> Unit) {
        if (loading) return
        loading = true
        scope.launch {
            try {
                asyncFn()
            } catch (e: Exception) {
                onError(e.message ?: e.toString())
            } finally {
                loading = false
            }
        }
    }
}
"""

    def create_feature_hook(self, pascal_name: str, snake_name: str) -> str:
        return f"""
package com.cleanarch.app.hooks

class Use{pascal_name} {{
    var loading = false
    var errorMsg = ""
}}
"""

    def create_ui_inspector(self) -> str:
        return """
package com.cleanarch.app.level_02_molecules.ui_inspector

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun UIInspector() {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .background(Color.Black.copy(alpha = 0.8f))
            .padding(8.dp),
        contentAlignment = Alignment.Center
    ) {
        Text(
            text = "UI Inspector (F11 to Capture)",
            color = Color.White,
            fontSize = 10.sp
        )
    }
}
"""

    def create_main_window(self, project_name: str) -> str:
        return f"""
package com.cleanarch.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import com.cleanarch.app.level_05_pages.WelcomeScreen

class MainActivity : ComponentActivity() {{
    override fun onCreate(savedInstanceState: Bundle?) {{
        super.onCreate(savedInstanceState)
        setContent {{
            WelcomeScreen()
        }}
    }}
}}
"""
