from netmiko import ConnectHandler

# Datos de conexión al CSR1000v
device = {
    'device_type': 'cisco_ios',
    'host': '192.168.56.107',
    'username': 'cisco',
    'password': 'cisco123!',
    'secret': 'cisco123!'
}

# Conexión SSH
net_connect = ConnectHandler(**device)
net_connect.enable()

print("✅ Conectado al router CSR1000v\n")

# Asegura que IPv6 esté habilitado
net_connect.send_config_set(["ipv6 unicast-routing"])

# Configuración EIGRP nombrado
eigrp_config = [
    "router eigrp EIGRP_NOMBRADO",
    "address-family ipv4 unicast autonomous-system 100",
    "network 192.168.0.0 0.0.255.255",
    "exit-address-family",

    "address-family ipv6 unicast autonomous-system 100",
    "eigrp router-id 1.1.1.1",
    "exit-address-family"
]

print("⚙️ Configurando EIGRP nombrado...\n")
cfg_output = net_connect.send_config_set(eigrp_config)
print(cfg_output)

# Ejecutar comandos de verificación
print("\n📄 Información recolectada del router:\n")

# 1. Sección EIGRP
eigrp_section = net_connect.send_command("show running-config | section eigrp")
print("🔍 EIGRP CONFIGURADO:\n")
print(eigrp_section)

# 2. Estado de interfaces
ip_int = net_connect.send_command("show ip interface brief")
print("\n🌐 IP INTERFACES:\n")
print(ip_int)

# 3. Running-config completo
run_config = net_connect.send_command("show running-config")
print("\n🧾 RUNNING-CONFIG (primeros 1000 caracteres):\n")
print(run_config[:1000] + "\n... [salida truncada]")

# 4. Versión del IOS
version_info = net_connect.send_command("show version")
print("\n💻 SHOW VERSION:\n")
print(version_info)

# Cierre de sesión
net_connect.disconnect()
print("\n🔒 Conexión cerrada.\n")
