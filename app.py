import requests
import subprocess
import re

router_address = '192.168.30.1'
server_address = '0.0.0.0'

def get_ip_prefixes_by_asn(asn):
    url = f"https://api.bgpview.io/asn/{asn}/prefixes"
    response = requests.get(url)
    data = response.json()
    ipv4_prefixes = [prefix['prefix'] for prefix in data['data']['ipv4_prefixes']]
    return ipv4_prefixes


def generate_exabgp_config(ip_prefixes, asn):
    routes = ""
    for prefix, community in ip_prefixes:
        routes += f"route {prefix} {{\n"
        routes += "    next-hop self;\n"
        routes += f"    community [ {asn}:{community} ];\n"
        routes += "}\n"

    config = f"""
    neighbor {router_address} {{
        router-id 192.168.30.2;
        local-as {asn};
        peer-as 65001;
        local-address {server_address};

        family {{
            ipv4 unicast;
        }}

        static {{
            {routes}
        }}
    }}
    """
    return config


if __name__ == '__main__':
    local_as = "65000"
    prefixes_with_communities = []
    with open("asList.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            asn_arr = line.strip("\n").split(":")
            if re.match("^[a-zA-Z0-9]*$", asn_arr[0]):
                asn = asn_arr[0]
                prefixes = get_ip_prefixes_by_asn(asn)
                community = int(asn_arr[1])
                for prefix in prefixes:
                    prefixes_with_communities.append([prefix, community])

    config = generate_exabgp_config(prefixes_with_communities, local_as)

    with open("exabgp.conf", "w+") as f:
        f.write(config)

    subprocess.run(["exabgp", "-d", "exabgp.conf"])