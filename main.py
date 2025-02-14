#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path
import pyfiglet

TEMP_FILE = "temp.txt"

def save_temp(decompiled=None, compiled=None):
    """Save decompiled and compiled paths to the temp file in the specified format."""
    # Ensure we write exactly:
    # Decompiled APK: <value>
    # Compiled APK: <value>
    with open(TEMP_FILE, "w") as f:
        f.write("Decompiled APK: " + (decompiled if decompiled else "") + "\n")
        f.write("Compiled APK: " + (compiled if compiled else "") + "\n")

def load_temp():
    """Load decompiled and compiled paths from the temp file.
    Returns (decompiled, compiled) or (None, None) if not found or broken."""
    if os.path.exists(TEMP_FILE):
        with open(TEMP_FILE, "r") as f:
            lines = f.read().splitlines()
        decompiled = None
        compiled = None
        if len(lines) >= 1 and lines[0].startswith("Decompiled APK:"):
            val = lines[0].split("Decompiled APK: ", 1)[1].strip()
            if val:
                decompiled = val
        if len(lines) >= 2 and lines[1].startswith("Compiled APK:"):
            val = lines[1].split("Compiled APK: ", 1)[1].strip()
            if val:
                compiled = val
        return decompiled, compiled
    return None, None

def clear_temp():
    if os.path.exists(TEMP_FILE):
        os.remove(TEMP_FILE)

def print_help():
    print("\nAvailable commands:")
    print("  help      - Show this help message")
    print("  about     - About this framework")
    print("  decompile - Decompile an APK using apktool")
    print("  compile   - Compile a decompiled folder using apktool by iBotPeaches")
    print("  patch     - Patch the decompiled APK (rename files and clean XML)")
    print("  sign      - Sign the compiled APK using uber-apk-signer by patrickfav")
    print("  exit      - Exit the framework\n")

def print_about():
    print("\nAndroid Reverse Engineer Framework v1.0")
    print("Author: Minhmc2007")
    print("A CLI tool for reversing Android APKs with decompiling, compiling, patching, and signing.\n")

def print_banner():
    banner = pyfiglet.figlet_format("Android Reverse Engineer Framework")
    print(banner)

def decompile_apk():
    apk_path = input("Enter the full path to the APK file: ").strip()
    if not os.path.exists(apk_path):
        print("Error: APK file not found!")
        return

    default_output = os.path.join(os.getcwd(), os.path.splitext(os.path.basename(apk_path))[0])
    output_dir = input(f"Enter output directory for decompiled files [default: {default_output}]: ").strip()
    if output_dir == "":
        output_dir = default_output

    print("\n[+] Starting decompilation...")
    try:
        subprocess.run(
            ["apktool", "d", apk_path, "-o", output_dir],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print(f"[+] Decompilation complete! Files saved to: {output_dir}\n")
        # Save the decompiled folder path and clear any previous compiled APK info.
        save_temp(decompiled=output_dir, compiled="")
    except subprocess.CalledProcessError:
        print("Error: apktool failed during decompilation.")

def compile_apk():
    temp_decompiled, _ = load_temp()
    prompt = "Enter the full path to the decompiled folder"
    if temp_decompiled:
        prompt += f" [default: {temp_decompiled}]"
    prompt += ": "
    decompiled_path = input(prompt).strip()
    if decompiled_path == "" and temp_decompiled:
        decompiled_path = temp_decompiled

    if not os.path.isdir(decompiled_path):
        print("Error: Specified folder not found!")
        return

    default_output_apk = os.path.join(os.getcwd(), "compiled.apk")
    output_apk = input(f"Enter output APK file path [default: {default_output_apk}]: ").strip()
    if output_apk == "":
        output_apk = default_output_apk

    print("\n[+] Starting compilation...")
    try:
        # Include the --aapt flag to use /usr/bin/aapt2
        result = subprocess.run(
            ["apktool", "b", decompiled_path, "-o", output_apk, "--aapt", "/usr/bin/aapt2"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"[+] Compilation complete! APK saved as: {output_apk}\n")
        print("[!] You may need to sign the APK before installation. Run 'sign' to sign the APK.\n")
        # Save both decompiled and compiled paths
        save_temp(decompiled=decompiled_path, compiled=output_apk)
    except subprocess.CalledProcessError as e:
        print("Error during compilation:")
        if e.stderr:
            print(e.stderr)
        else:
            print("Unknown error.")
        print("\n[!] You may need to run 'patch' before compiling to fix potential issues in the decompiled files.\n")

def rename_files_recursively(root_dir):
    """Rename files in the given directory, removing '$' from filenames."""
    for root, _, files in os.walk(root_dir):
        for filename in files:
            if "$" in filename:
                new_name = filename.replace("$", "")
                old_path = os.path.join(root, filename)
                new_path = os.path.join(root, new_name)
                os.rename(old_path, new_path)
                print(f"[+] Renamed: {filename} → {new_name}")

def clean_xml_content(root_dir):
    """Remove '$' from all XML files in the given directory."""
    root_path = Path(root_dir)
    if not root_path.exists():
        print(f"[-] Directory not found: {root_dir}")
        return

    cleaned_files = 0
    error_files = 0
    skipped_files = 0

    for xml_file in root_path.rglob("*.xml"):
        try:
            with open(xml_file, "r", encoding="utf-8") as f:
                content = f.read()
            cleaned = content.replace("$", "")
            if cleaned != content:
                with open(xml_file, "w", encoding="utf-8") as f:
                    f.write(cleaned)
                print(f"[+] Cleaned: {xml_file}")
                cleaned_files += 1
            else:
                skipped_files += 1
        except UnicodeDecodeError:
            print(f"[!] Encoding error in {xml_file}. Trying with 'latin-1' encoding...")
            try:
                with open(xml_file, "r", encoding="latin-1") as f:
                    content = f.read()
                cleaned = content.replace("$", "")
                if cleaned != content:
                    with open(xml_file, "w", encoding="utf-8") as f:
                        f.write(cleaned)
                    print(f"[+] Cleaned (latin-1): {xml_file}")
                    cleaned_files += 1
                else:
                    skipped_files += 1
            except Exception as e:
                print(f"[-] Failed to process {xml_file} with latin-1 encoding: {str(e)}")
                error_files += 1
        except Exception as e:
            print(f"[-] Error processing {xml_file}: {str(e)}")
            error_files += 1

    print("\n[+] Patch Summary:")
    print(f"  - Files cleaned: {cleaned_files}")
    print(f"  - Files skipped: {skipped_files}")
    print(f"  - Files with errors: {error_files}")
    print(f"  - Total processed: {cleaned_files + skipped_files + error_files}\n")

def run_patch():
    """Run renaming and XML cleaning on the decompiled APK's 'res' folder."""
    temp_decompiled, _ = load_temp()
    if not temp_decompiled:
        print("[-] No decompiled APK found. Run 'decompile' first.")
        return

    res_folder = os.path.join(temp_decompiled, "res")
    if not os.path.exists(res_folder):
        print("[-] 'res' folder not found in the decompiled APK!")
        return

    print(f"\n[+] Running patch scripts on: {res_folder}")
    rename_files_recursively(res_folder)
    clean_xml_content(res_folder)
    print("[+] Patching complete!\n")

def sign_apk():
    """Sign the compiled APK using sign.jar."""
    _, temp_compiled = load_temp()
    prompt = "Enter the full path to the APK to sign"
    if temp_compiled:
        prompt += f" [default: {temp_compiled}]"
    prompt += ": "
    apk_to_sign = input(prompt).strip()
    if apk_to_sign == "" and temp_compiled:
        apk_to_sign = temp_compiled

    if not os.path.exists(apk_to_sign):
        print("Error: APK file not found!")
        return

    print("\n[+] Starting APK signing...")
    try:
        subprocess.run(
            ["java", "-jar", "sign.jar", "--apks", apk_to_sign],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("[+] APK signing complete!\n")
    except subprocess.CalledProcessError:
        print("Error: APK signing failed.")

def main():
    print_banner()
    print("Welcome to the Android Reverse Engineer Framework!")
    print("Type 'help' for a list of commands.\n")
    
    while True:
        try:
            command = input("android_re> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            break

        if command == "help":
            print_help()
        elif command == "about":
            print_about()
        elif command == "decompile":
            decompile_apk()
        elif command == "compile":
            compile_apk()
        elif command == "patch":
            run_patch()
        elif command == "sign":
            sign_apk()
        elif command in ["exit", "quit"]:
            print("Exiting framework...")
            break
        else:
            print("Unknown command. Type 'help' for available commands.")
    
    clear_temp()

if __name__ == "__main__":
    main()
