# main.py
import network
import urequests
import time
import ubinascii
from machine import Pin, SPI
import ili9341
import ui_pack

# Variables
WIFI_SSID = ""
WIFI_PASS = ""

ADGUARD_IP   = ""
ADGUARD_PORT = ""
ADGUARD_USER = ""
ADGUARD_PASS = ""

DEBUG = False

# ESP-WROOM-32 connections

# VCC - 3v
# GND - GND
# CS - D15
# RESET - D4
# DC - D2
# SDI(mosi) - D23
# SCK - D18
# LED - 3v
# SDO(mosi) - D19

vspi = SPI(1, baudrate=20000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
display = ili9341.Display(vspi, dc=Pin(2), cs=Pin(15), rst=Pin(4), width=320, height=240, rotation=90)

gui = ui_pack.ModernUI(display)

# ================= FONCTIONS =================

def connect_wifi():
    display.clear()
    display.draw_text8x8(10, 10, "Wifi connection...", gui.WHITE)
    wlan = network.WLAN(network.WLAN.IF_STA)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            time.sleep(0.5)
    
    display.draw_text8x8(10, 10, 'IP:{}'.format(wlan.ifconfig()[0]), gui.WHITE)
    time.sleep(1)
    display.clear()

def init_dashboard_static():
    display.clear()
    
    display.fill_rectangle(0, 0, 320, 40, gui.GREEN)
    display.draw_text8x8(100, 15, "ADGUARD HOME", gui.BLACK, gui.GREEN)
    
    display.fill_rectangle(0, 40, 320, 200, gui.BLACK)

    gui.draw_card_static(10, 50, 145, 100, "TOTAL", "DNS QUERIES")
    gui.draw_card_static(165, 50, 145, 100, "BLOCKED", "ADS")
    display.draw_text8x8(10, 170, "Blocked by Filters:", gui.WHITE, gui.BLACK)
    
    gui.draw_bar_static(10, 190, 300, 20)


def update_dashboard_values(stats):
    total = stats.get("num_dns_queries", 0)
    blocked = stats.get("num_blocked_filtering", 0)
    
    percent = 0
    if total > 0:
        percent = (blocked / total) * 100
        
    gui.update_card_value(10, 50, 145, total, gui.GREEN)
    gui.update_card_value(165, 50, 145, blocked, gui.RED)
    
    display.fill_rectangle(165, 170, 60, 10, gui.BLACK)
    
    p_color = gui.GREEN if percent < 10 else gui.RED
    display.draw_text8x8(165, 170, "{:.1f}%".format(percent), p_color, gui.BLACK)
    
    gui.update_progress_bar(10, 190, 300, 20, percent, p_color)
    
def get_adguard_stats():
    url = "http://{}:{}/control/stats".format(ADGUARD_IP, ADGUARD_PORT)
    auth_str = "{}:{}".format(ADGUARD_USER, ADGUARD_PASS)
    auth_b64 = ubinascii.b2a_base64(auth_str).strip()
    
    headers = {
        'Authorization': b'Basic ' + auth_b64,
        'Content-Type': 'application/json'
    }
    
    if DEBUG == True:
        print("GET:", url)
    else:
        pass
    try:
        resp = urequests.get(url, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            resp.close()
            return data
        else:
            print("HTTP Error:", resp.status_code)
            resp.close()
            return None
    except Exception as e:
        print("Error:", e)
        return None

def draw_dashboard_landscape(stats):
    display.fill_rectangle(0, 40, 320, 200, gui.BLACK)

    total = stats.get("num_dns_queries", 0)
    blocked = stats.get("num_blocked_filtering", 0)
    
    if DEBUG == True:
        print("total: ", total, '\n', "blocked: ", blocked)
    else:
        pass
    
    percent = 0
    if total > 0:
        percent = (blocked / total) * 100
        
    #---------------------------------------
    #               INFO CARDS
    #---------------------------------------
    gui.draw_card(10, 50, 145, 100, "TOTAL", total, "DNS QUERIES", gui.GREEN)
    gui.draw_card(165, 50, 145, 100, "BLOQUE", blocked, "PUBS", gui.RED)
    
    #---------------------------------------
    #    PROGRESS_BAR BLOCKED QUERIES
    #---------------------------------------
    display.draw_text8x8(10, 170, "Blocked by Filters:", gui.WHITE, gui.BLACK)
    
    p_color = gui.GREEN if percent < 10 else gui.RED
    display.draw_text8x8(165, 170, "{:.1f}%".format(percent), p_color, gui.BLACK)
    
    gui.draw_progress_bar(10, 190, 300, 20, percent, p_color)

def main():
    connect_wifi()
    time.sleep(1)
    
    if DEBUG == True:
        print("Dashboard init...")
    else :
        pass
    init_dashboard_static()
    
    while True:
        if DEBUG == True:
            print("Update...")
        else:
            pass
        stats = get_adguard_stats()
        
        if stats:
            update_dashboard_values(stats)
        else:
            display.fill_rectangle(300, 220, 20, 20, gui.RED)
            
        time.sleep(5)

main()
