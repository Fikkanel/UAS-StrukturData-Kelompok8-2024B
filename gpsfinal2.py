import heapq
import itertools
import time
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from colorama import Fore, Back, Style, init

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# --- Data kota dan edges ---
kota = [
    "Surabaya", "Sidoarjo", "Gresik", "Lamongan", "Mojokerto",
    "Pasuruan", "Malang", "Probolinggo", "Bangkalan", "Jombang"
]

edges = [
    ("Surabaya", "Sidoarjo", 20), ("Surabaya", "Gresik", 15), ("Surabaya", "Bangkalan", 25),
    ("Sidoarjo", "Mojokerto", 30), ("Sidoarjo", "Pasuruan", 35), ("Sidoarjo", "Jombang", 40),
    ("Gresik", "Lamongan", 20), ("Gresik", "Bangkalan", 30), ("Gresik", "Malang", 50),
    ("Lamongan", "Jombang", 45), ("Lamongan", "Mojokerto", 25), ("Lamongan", "Probolinggo", 60),
    ("Mojokerto", "Malang", 40), ("Mojokerto", "Pasuruan", 30), ("Mojokerto", "Jombang", 15),
    ("Pasuruan", "Probolinggo", 20), ("Pasuruan", "Malang", 25), ("Pasuruan", "Jombang", 35),
    ("Malang", "Probolinggo", 30), ("Malang", "Bangkalan", 60), ("Malang", "Jombang", 20),
    ("Probolinggo", "Bangkalan", 55), ("Probolinggo", "Lamongan", 45), ("Probolinggo", "Jombang", 50),
    ("Bangkalan", "Jombang", 65), ("Bangkalan", "Lamongan", 30), ("Surabaya", "Malang", 40),
    ("Surabaya", "Jombang", 35), ("Surabaya", "Pasuruan", 50), ("Sidoarjo", "Probolinggo", 45)
]

# --- Membuat adjacency list ---
graph = {city: {} for city in kota}
for u, v, w in edges:
    graph[u][v] = w
    graph[v][u] = w

# --- Fungsi untuk print dengan style ---
def print_header(text, color=Fore.CYAN, style=Style.BRIGHT):
    """Print header dengan style menarik"""
    border = "=" * (len(text) + 4)
    print(f"\n{color}{style}{border}")
    print(f"  {text}")
    print(f"{border}{Style.RESET_ALL}")

def print_box(text, color=Fore.GREEN, padding=2):
    """Print text dalam box"""
    lines = text.split('\n')
    max_width = max(len(line) for line in lines)
    border = "+" + "-" * (max_width + padding * 2) + "+"
    
    print(f"{color}{border}")
    for line in lines:
        print(f"{color}|{' ' * padding}{line:<{max_width}}{' ' * padding}|")
    print(f"{color}{border}{Style.RESET_ALL}")

def print_route_animation(route, title="🛣️ RUTE PERJALANAN"):
    """Print rute dengan animasi arrow"""
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}{title}{Style.RESET_ALL}")
    print("┌" + "─" * 60 + "┐")
    
    route_display = ""
    for i, city in enumerate(route):
        if i == 0:
            route_display += f"{Fore.GREEN}🏁 {city}{Style.RESET_ALL}"
        elif i == len(route) - 1:
            route_display += f" {Fore.RED}➤{Style.RESET_ALL} {Fore.RED}🏆 {city}{Style.RESET_ALL}"
        else:
            route_display += f" {Fore.BLUE}➤{Style.RESET_ALL} {Fore.CYAN}{city}{Style.RESET_ALL}"
    
    print(f"│ {route_display:<50} │")
    print("└" + "─" * 60 + "┘")

def print_distance_info(distance, color=Fore.MAGENTA):
    """Print info jarak dengan style"""
    print(f"\n{color}{Style.BRIGHT}📏 TOTAL JARAK: {distance} km{Style.RESET_ALL}")
    print(f"{color}{'🚗 ' * (min(distance // 10, 10))}{Style.RESET_ALL}")

def print_loading_animation():
    """Print loading animation"""
    print(f"\n{Fore.YELLOW}🔄 Menghitung rute optimal", end="")
    for i in range(3):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print(f" {Fore.GREEN}✓ Selesai!{Style.RESET_ALL}")

def print_city_list():
    """Print daftar kota dengan style"""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}🏙️ DAFTAR KOTA TERSEDIA:{Style.RESET_ALL}")
    cities_per_row = 5
    for i in range(0, len(kota), cities_per_row):
        row_cities = kota[i:i + cities_per_row]
        city_display = " | ".join([f"{Fore.YELLOW}{city}{Style.RESET_ALL}" for city in row_cities])
        print(f"   {city_display}")

# --- Algoritma Dijkstra ---
def dijkstra_shortest_path(graph, start, end):
    queue = [(0, start, [start])]
    visited = set()
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    while queue:
        cost, node, path = heapq.heappop(queue)
        if node in visited:
            continue
        visited.add(node)
        if node == end:
            return cost, path
        for neighbor, weight in graph[node].items():
            if neighbor not in visited:
                new_cost = cost + weight
                if new_cost < distances[neighbor]:
                    distances[neighbor] = new_cost
                    heapq.heappush(queue, (new_cost, neighbor, path + [neighbor]))
    return float('inf'), []

# --- Hitung jarak total rute ---
def calculate_route_distance(graph, route):
    total = 0
    for i in range(len(route) - 1):
        dist = graph[route[i]].get(route[i+1], float('inf'))
        if dist == float('inf'):
            return float('inf')
        total += dist
    return total

# --- Brute-force TSP tanpa kembali ke start ---
def tsp_brute_force(graph, start):
    nodes = list(graph.keys())
    nodes.remove(start)
    best_route = None
    best_cost = float('inf')

    print_header("🧮 PERHITUNGAN TSP DIMULAI", Fore.MAGENTA)
    print(f"{Fore.YELLOW}⚙️ Menganalisis {len(list(itertools.permutations(nodes)))} kemungkinan rute...{Style.RESET_ALL}")
    
    start_time = time.time()
    total_perms = len(list(itertools.permutations(nodes)))
    processed = 0

    for perm in itertools.permutations(nodes):
        route = [start] + list(perm)
        cost = calculate_route_distance(graph, route)
        if cost < best_cost:
            best_cost = cost
            best_route = route
        
        processed += 1
        if processed % 10000 == 0:
            progress = (processed / total_perms) * 100
            print(f"{Fore.CYAN}📊 Progress: {progress:.1f}% ({processed}/{total_perms}){Style.RESET_ALL}")

    end_time = time.time()
    print(f"\n{Fore.GREEN}✅ Perhitungan selesai dalam {end_time - start_time:.2f} detik{Style.RESET_ALL}")
    return best_route, best_cost

# --- Fungsi input dan jalankan Dijkstra ---
def run_dijkstra():
    print_header("🎯 ALGORITMA DIJKSTRA - RUTE TERCEPAT", Fore.BLUE)
    print_city_list()
    
    while True:
        start = input(f"\n{Fore.GREEN}🏁 Masukkan kota asal: {Style.RESET_ALL}").strip().title()
        if start in kota:
            print(f"{Fore.GREEN}✓ Kota asal: {start}{Style.RESET_ALL}")
            break
        print(f"{Fore.RED}❌ Kota '{start}' tidak ditemukan, coba lagi.{Style.RESET_ALL}")
    
    while True:
        end = input(f"{Fore.RED}🏆 Masukkan kota tujuan: {Style.RESET_ALL}").strip().title()
        if end in kota:
            print(f"{Fore.RED}✓ Kota tujuan: {end}{Style.RESET_ALL}")
            break
        print(f"{Fore.RED}❌ Kota '{end}' tidak ditemukan, coba lagi.{Style.RESET_ALL}")
    
    if start == end:
        print_box(f"🏠 Kota asal dan tujuan sama\n📏 Jarak: 0 km", Fore.YELLOW)
        return start, [start]
    
    print_loading_animation()
    dist, path = dijkstra_shortest_path(graph, start, end)
    
    if dist == float('inf'):
        print_box("❌ Tidak ada rute yang tersedia", Fore.RED)
        return start, []
    else:
        print_route_animation(path, "🛣️ RUTE TERCEPAT DITEMUKAN")
        print_distance_info(dist)
        return start, path

# --- Fungsi input dan jalankan TSP ---
def run_tsp():
    print_header("🌍 TRAVELING SALESMAN PROBLEM (TSP)", Fore.MAGENTA)
    print_box("🎯 Tujuan: Mengunjungi semua kota tepat sekali\n📍 Tanpa kembali ke kota asal", Fore.CYAN)
    print_city_list()
    
    while True:
        start = input(f"\n{Fore.GREEN}🏁 Masukkan kota awal untuk TSP: {Style.RESET_ALL}").strip().title()
        if start in kota:
            print(f"{Fore.GREEN}✓ Kota awal: {start}{Style.RESET_ALL}")
            break
        print(f"{Fore.RED}❌ Kota '{start}' tidak ditemukan, coba lagi.{Style.RESET_ALL}")
    
    route, dist = tsp_brute_force(graph, start)
    
    if route:
        print_route_animation(route, "🏆 RUTE TSP OPTIMAL")
        print_distance_info(dist)
        
        # Tampilkan detail perjalanan
        print(f"\n{Fore.CYAN}{Style.BRIGHT}📋 DETAIL PERJALANAN:{Style.RESET_ALL}")
        for i in range(len(route) - 1):
            segment_dist = graph[route[i]][route[i+1]]
            print(f"   {Fore.YELLOW}{i+1}.{Style.RESET_ALL} {route[i]} → {route[i+1]} ({segment_dist} km)")
        
        return route
    else:
        print_box("❌ Tidak ditemukan rute TSP yang valid", Fore.RED)
        return None

# --- Menampilkan semua jarak antar kota ---
def show_all_distances():
    print_header("📊 MATRIKS JARAK ANTAR KOTA", Fore.CYAN)
    
    # Group edges by distance for better readability
    short_routes = []
    medium_routes = []
    long_routes = []
    
    for u, v, w in edges:
        if w <= 25:
            short_routes.append((u, v, w))
        elif w <= 45:
            medium_routes.append((u, v, w))
        else:
            long_routes.append((u, v, w))
    
    print(f"\n{Fore.GREEN}{Style.BRIGHT}🟢 JARAK PENDEK (≤ 25 km):{Style.RESET_ALL}")
    for u, v, w in sorted(short_routes, key=lambda x: x[2]):
        print(f"   {Fore.GREEN}{u} ↔ {v} = {w} km{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}🟡 JARAK SEDANG (26-45 km):{Style.RESET_ALL}")
    for u, v, w in sorted(medium_routes, key=lambda x: x[2]):
        print(f"   {Fore.YELLOW}{u} ↔ {v} = {w} km{Style.RESET_ALL}")
    
    print(f"\n{Fore.RED}{Style.BRIGHT}🔴 JARAK JAUH (> 45 km):{Style.RESET_ALL}")
    for u, v, w in sorted(long_routes, key=lambda x: x[2]):
        print(f"   {Fore.RED}{u} ↔ {v} = {w} km{Style.RESET_ALL}")
    
    print(f"\n{Fore.MAGENTA}📈 STATISTIK:{Style.RESET_ALL}")
    all_distances = [w for _, _, w in edges]
    print(f"   • Total rute: {len(edges)}")
    print(f"   • Jarak terpendek: {min(all_distances)} km")
    print(f"   • Jarak terjauh: {max(all_distances)} km")
    print(f"   • Rata-rata: {sum(all_distances)/len(all_distances):.1f} km")

# --- Visualisasi graf dan rute ---
def visualize_graph(graph, dijkstra_path=None, tsp_path=None):
    print_header("📈 MEMBUAT VISUALISASI GRAF", Fore.MAGENTA)
    
    G = nx.Graph()
    for u in graph:
        for v, w in graph[u].items():
            if not G.has_edge(u, v):
                G.add_edge(u, v, weight=w)

    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', 
            node_size=2500, font_size=9, font_weight='bold')
    
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    # Highlight paths
    if dijkstra_path and len(dijkstra_path) > 1:
        dijkstra_edges = [(dijkstra_path[i], dijkstra_path[i+1]) for i in range(len(dijkstra_path)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=dijkstra_edges, edge_color='red', width=3)
    
    if tsp_path and len(tsp_path) > 1:
        tsp_edges = [(tsp_path[i], tsp_path[i+1]) for i in range(len(tsp_path)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=tsp_edges, edge_color='green', width=2)

    plt.title("🗺️ Peta Rute Jawa Timur\n🔴 Dijkstra | 🟢 TSP", fontsize=14, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.show()
    
    print(f"{Fore.GREEN}✅ Visualisasi berhasil ditampilkan!{Style.RESET_ALL}")

# --- Menu dengan style ---
def print_menu():
    menu_text = """
1️⃣  Cari rute tercepat (Dijkstra)
2️⃣  Cari rute Traveling Salesman Problem (TSP)  
3️⃣  Cari keduanya (Dijkstra + TSP)
4️⃣  Lihat detail jarak antar kota
5️⃣  Keluar dari program
"""
    print_box(menu_text.strip(), Fore.CYAN)

# --- Program utama dengan menu pilihan ---
def main():
    # Header utama
    print(f"\n{Back.BLUE}{Fore.WHITE}{Style.BRIGHT}")
    print("=" * 60)
    print("🗺️           PETA DAN GPS JAWA TIMUR           🗺️".center(60))
    print("=" * 60)
    print(f"{Style.RESET_ALL}")
    
    info_text = """
🏙️  Jumlah Kota: 10 kota
🛣️  Jumlah Jalur: 30 rute
📏  Satuan: Kilometer
🎯  Algoritma: Dijkstra & TSP
"""
    print_box(info_text.strip(), Fore.YELLOW)

    dijkstra_path = None
    tsp_path = None

    while True:
        print(f"\n{Fore.MAGENTA}{Style.BRIGHT}🎮 MENU NAVIGASI{Style.RESET_ALL}")
        print_menu()

        pilihan = input(f"\n{Fore.CYAN}👉 Pilih menu (1-5): {Style.RESET_ALL}").strip()
        
        if pilihan == "1":
            _, dijkstra_path = run_dijkstra()
            tsp_path = None
        elif pilihan == "2":
            tsp_path = run_tsp()
            dijkstra_path = None
        elif pilihan == "3":
            print_header("🎯 ANALISIS LENGKAP: DIJKSTRA + TSP", Fore.MAGENTA)
            _, dijkstra_path = run_dijkstra()
            tsp_path = run_tsp()
        elif pilihan == "4":
            show_all_distances()
        elif pilihan == "5":
            print_header("👋 TERIMA KASIH!", Fore.GREEN)
            print_box("Program GPS Jawa Timur selesai.\nSemoga perjalanan Anda menyenangkan! 🚗💨", Fore.GREEN)
            break
        else:
            print_box("❌ Pilihan tidak valid!\n👉 Silakan pilih angka 1-5", Fore.RED)
            continue
        
        if dijkstra_path or tsp_path:
            show_viz = input(f"\n{Fore.CYAN}📊 Tampilkan visualisasi graf? (y/n): {Style.RESET_ALL}").strip().lower()
            if show_viz in ['y', 'yes', 'ya']:
                visualize_graph(graph, dijkstra_path=dijkstra_path, tsp_path=tsp_path)

if __name__ == "__main__":
    main()