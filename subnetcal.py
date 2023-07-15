import ipaddress


def calculate_network_details(ip_address, netmask):
    network = ipaddress.IPv4Network(f"{ip_address}/{netmask}", strict=False)
    network_id = network.network_address
    broadcast = network.broadcast_address
    wildcard = ipaddress.IPv4Address(int(network_id) ^ int(broadcast))
    min_host = network.network_address + 1
    max_host = network.broadcast_address - 1
    host_count = network.num_addresses - 2
    ip_class = None

    class_a = ipaddress.IPv4Network(("10.0.0.0", "255.0.0.0"))
    class_b = ipaddress.IPv4Network(("172.16.0.0", "255.240.0.0"))
    class_c = ipaddress.IPv4Network(("192.168.0.0", "255.255.0.0"))

    if ip_address in class_a:
        ip_class = "Class A"
    elif ip_address in class_b:
        ip_class = "Class B"
    elif ip_address in class_c:
        ip_class = "Class C"

    return network_id, broadcast, wildcard, min_host, max_host, host_count, network, ip_class


while True:
    try:
        # ip_address = "10.0.20.0"
        ip_address = input("Enter the IP address: ")
        # netmask = int("30")
        netmask = int("".join(filter(str.isdigit, input("Enter the netmask: "))))
        ip_address = ipaddress.ip_address(ip_address)
        break
    except ValueError:
        input("Invalid input, Try again.")

network_id, broadcast, wildcard, min_host, max_host, \
    host_count, network, ip_class = calculate_network_details(ip_address, netmask)

network_bit = {key: bin(int(value))[2:].zfill(32)
               for key, value in {'address_bit': ip_address, 'wildcard_bit': wildcard,
                                  'network_bit': network_id, 'broadcast_bit': broadcast,
                                  'hostmin_bit': min_host, 'hostmax_bit': max_host}.items()}

network_dot = {key: '.'.join([value[i:i + 8] for i in range(0, 32, 8)])
               for key, value in network_bit.items()}

netmask_bit = "1" * netmask
netmask_bit = netmask_bit[::-1].zfill(32)[::-1]
netmask_bit = '.'.join([netmask_bit[i:i + 8] for i in range(0, 32, 8)])

print(f"Address:   {str(ip_address):<15} {network_dot['address_bit']}")
print(f"Netmask:   {str(network.netmask):<15} {netmask_bit} = {netmask}")
print(f"Wildcard:  {str(wildcard):<15} {network_dot['wildcard_bit']}")
print(f"\nNetwork:   {str(network_id)}/{netmask:<5} {network_dot['network_bit']} ({ip_class})")
print(f"Broadcast: {str(broadcast):<15} {network_dot['broadcast_bit']}")
print(f"HostMin:   {str(min_host):<15} {network_dot['hostmin_bit']}")
print(f"HostMax:   {str(max_host):<15} {network_dot['hostmax_bit']}")
print(f"Hosts/Net: {host_count:<15} {'Private IP' if ip_address.is_private else 'Not Private IP'}")
