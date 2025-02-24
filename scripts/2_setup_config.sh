#!/bin/bash

# Configure Prompt Engineering Lab
ROOT_DIR="$(cd "$(dirname "$0")"/.. && pwd)"
EXAMPLE_FILE=$(find "$ROOT_DIR" -type f -name "_config.example" ! -path "*/.*" ! -path "*/GENAIENV/*" ! -path "*/__pycache__/*" | head -n 1)

if [[ -z "$EXAMPLE_FILE" ]]; then
    echo "⚠️ No '_config.example' found. Please ensure it exists."
    exit 1
fi

CONFIG_DIR=$(dirname "$EXAMPLE_FILE")
CONFIG_FILE="$CONFIG_DIR/_config"

# Check if _config already exists
if [[ -f "$CONFIG_FILE" ]]; then
    read -rp "_config already exists. Replace it with new settings? (y/n): " replace_config
    if [[ ! $replace_config =~ ^[Yy]$ ]]; then
        echo "🛑 Keeping existing _config."
        exit 0
    fi
    rm -f "$CONFIG_FILE"
fi

# Copy the template config file
cp "$EXAMPLE_FILE" "$CONFIG_FILE"
echo "✅ Created _config file from template."

# Prompt for server selection
echo -e "\nSelect the Ollama server type:"
echo "1) Local Ollama (localhost)"
echo "2) FAU HPC Server"
read -rp "Enter your choice (1/2): " server_choice

# Update the config based on the selection
if [[ "$server_choice" == "1" ]]; then
    # Switch to Local Ollama
    awk '{gsub(/^#URL_GENERATE=http:\/\/localhost:11434/, "URL_GENERATE=http://localhost:11434"); gsub(/^URL_GENERATE=https:\/\/chat.hpc.fau.edu/, "#URL_GENERATE=https://chat.hpc.fau.edu"); gsub(/^API_KEY=.*/, "#API_KEY="); print}' "$CONFIG_FILE" > tmpfile && mv tmpfile "$CONFIG_FILE"
    echo "✅ Configuration updated for Local Ollama."

elif [[ "$server_choice" == "2" ]]; then
    # Switch to FAU Server
    awk '{gsub(/^URL_GENERATE=http:\/\/localhost:11434/, "#URL_GENERATE=http://localhost:11434"); gsub(/^#URL_GENERATE=https:\/\/chat.hpc.fau.edu/, "URL_GENERATE=https://chat.hpc.fau.edu"); print}' "$CONFIG_FILE" > tmpfile && mv tmpfile "$CONFIG_FILE"

    # Ask for the API key
    while true; do
        read -rp "Do you have an FAU API key? (y/n): " api_choice
        if [[ "$api_choice" =~ ^[Nn]$ ]]; then
            echo "📖 Please refer to 'docs/CONFIG-FAU.md' to get your API key."
            read -rp "Press Enter once you have the key..."
        fi

        read -rp "Enter your FAU API key: " api_key
        if [[ -n "$api_key" ]]; then
            # Ensure API_KEY line exists and update it
            if grep -q '^#API_KEY=' "$CONFIG_FILE"; then
                awk -v key="$api_key" '{gsub(/^#API_KEY=.*/, "API_KEY="key); print}' "$CONFIG_FILE" > tmpfile && mv tmpfile "$CONFIG_FILE"
            else
                echo "API_KEY=$api_key" >> "$CONFIG_FILE"
            fi
            echo "✅ FAU configuration updated with the provided API key."
            break
        else
            echo "⚠️ No API key entered. Please try again."
        fi
    done

else
    echo "❌ Invalid selection. Defaulting to Local Ollama."
    awk '{gsub(/^#URL_GENERATE=http:\/\/localhost:11434/, "URL_GENERATE=http://localhost:11434"); gsub(/^URL_GENERATE=https:\/\/chat.hpc.fau.edu/, "#URL_GENERATE=https://chat.hpc.fau.edu"); gsub(/^API_KEY=.*/, "#API_KEY="); print}' "$CONFIG_FILE" > tmpfile && mv tmpfile "$CONFIG_FILE"
    echo "✅ Defaulted to Local Ollama."
fi

echo "🎯 Configuration completed successfully."

# Show final config state
echo -e "\n🔍 Final configuration:"
cat "$CONFIG_FILE"

# Ask if the user wants to test the new configuration
read -rp "Would you like to test the new configuration now? (y/n): " run_test

if [[ "$run_test" =~ ^[Yy]$ ]]; then
    bash "$ROOT_DIR/scripts/4_setup_llm_test.sh"
else
    echo "🟢 Configuration complete. Environment is ready for use."
    # Activate environment
    if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        source "$ROOT_DIR/GENAIENV/Scripts/activate"
    else
        source "$ROOT_DIR/GENAIENV/bin/activate"
    fi
    echo "✅ Virtual environment 'GENAIENV' activated. Follow the README instructions for usage."
fi
