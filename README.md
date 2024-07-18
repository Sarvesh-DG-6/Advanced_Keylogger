# Advanced Keylogger:
A Keylogger malware which collects and saves Key Logs, Clipboard, System Information, and Window Screenshot of the victim. 

# Steps:
1. Generate a Fernet Key running the generate_key.py
2. Copy the key from encrypt_key.txt and put it in the keylogger.py
3. Run the keylogger.py and observe the malware process
  
# Description:
Understanding the working of a real-time keylogger malware. 
When the malicious code is executed, it starts capturing real-time information from the victim's system in various file formats. 
A Fernet key is generated to encrypt these files. 
Then the encrypted files are sent to the attacker via email service (SMTP) while the actual files are saved in the victim's system.
