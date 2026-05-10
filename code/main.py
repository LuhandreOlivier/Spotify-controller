import urequests as requests
import secrets  # Ensure your secrets file has the necessary tokens and credentials
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
from machine import I2C, Pin
import time
import gc

# LCD configuration
I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=100000)  # Adjust pin numbers as needed
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
lcd.putstr("Welcome")

# Button configuration
PIN_VOL_UP = 5
PIN_VOL_DOWN = 6
PIN_PLAY_PAUSE = 4
PIN_NEXT_TRACK = 2
PIN_PREV_TRACK = 15

# Setup buttons as inputs
button_vol_up = Pin(PIN_VOL_UP, Pin.IN, Pin.PULL_UP)
button_vol_down = Pin(PIN_VOL_DOWN, Pin.IN, Pin.PULL_UP)
button_play_pause = Pin(PIN_PLAY_PAUSE, Pin.IN, Pin.PULL_UP)
button_next_track = Pin(PIN_NEXT_TRACK, Pin.IN, Pin.PULL_UP)
button_prev_track = Pin(PIN_PREV_TRACK, Pin.IN, Pin.PULL_UP)

# State variables
flag_button = False  # Flag to indicate button press
pressed_pin = None  # Pin number of the pressed button
volume = 50  # Start volume value
debounce_time = 3000
last_button_time = time.ticks_ms()  # For debounce checking
last_api_call_time = time.ticks_ms()  # For API call rate limiting
clear_line = "                ";

def update_track(track_substring):
    global lcd_track
    try:
        lcd.move_to(0, 0)
        lcd.putstr(track_substring[0:16])
    except OSError as e:
        print(f"Error updating track on LCD: {e}")
        handle_lcd_error()
    lcd_track = track_substring
        
def update_artist(artist_substring):
    global lcd_artist
    try:
        lcd.move_to(0, 1)
        lcd.putstr(artist_substring[0:16])
    except OSError as e:
        print(f"Error updating track on LCD: {e}")
        handle_lcd_error()
    lcd_artist = artist_substring
    

def update_lcd(track, artist):
    global lcd_track, lcd_artist
    try:
        if len(track) > 16:
            track = track[0:16]
        if len(artist) > 16:
            artist = artist[0:16]
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr(track)
        lcd.move_to(0, 1)
        lcd.putstr(artist)
    except OSError as e:
        print(f"Error updating track on LCD: {e}")
        handle_lcd_error()
    lcd_track = track
    lcd_artist = artist

def handle_lcd_error():
    global i2c, lcd
    try:
        # Re-initialize the I2C and LCD to reset communication
        i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=100000)  # Reduce frequency to 100kHz
        lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
        lcd.clear()
        lcd.putstr("Reconnected")
        time.sleep(1)
    except Exception as e:
        print(f"Failed to reinitialize LCD: {e}")


def simple_base64_encode(data):
    import binascii
    def b64encode(data):
        alphabet = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        padding = b"="
        data = binascii.b2a_base64(data).rstrip(b'\n')
        padding_len = (4 - len(data) % 4) % 4
        return data + (padding * padding_len)
    
    return b64encode(data.encode('utf-8')).decode('utf-8')

def encode_auth_header(client_id, client_secret):
    auth_str = f"{client_id}:{client_secret}"
    return simple_base64_encode(auth_str)

def get_current_track(access_token):
    ensure_wifi()  # Ensure Wi-Fi connection before making the API call
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    response = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers=headers)
    print(response)  # Debugging
    gc.collect()  # Free up memory after the request

    if response.status_code == 200:
        data = response.json()
        if not data or 'item' not in data:
            print("No track data available.")
            return "None", "None", 0, 0
        
        track_name = data['item'].get('name', 'Unknown')
        artist_name = ', '.join(artist['name'] for artist in data['item'].get('artists', []))
        duration_ms = data['item'].get('duration_ms', 0)
        progress_ms = data.get('progress_ms', 0)
        return track_name, artist_name, duration_ms, progress_ms
    elif response.status_code == 401:
        print("Access token expired. Refreshing token...")
        new_access_token, new_refresh_token = refresh_access_token(secrets.REFRESH_TOKEN)
        if new_access_token:
            secrets.ACCESS_TOKEN = new_access_token
            return get_current_track(new_access_token)
        else:
            print("Failed to refresh access token.")
            return None, None, None, None
    else:
        print(f"Failed to get data: {response.status_code}")
        print(f"Response content: {response.text}")
        return None, None, None, None


def refresh_access_token(refresh_token):
    auth_url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + encode_auth_header(secrets.CLIENT_ID, secrets.CLIENT_SECRET),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = 'grant_type=refresh_token&refresh_token=' + refresh_token
    response = requests.post(auth_url, headers=headers, data=data)
    
    if response.status_code == 200:
        tokens = response.json()
        return tokens.get('access_token'), tokens.get('refresh_token')
    else:
        print(f"Failed to refresh token: {response.status_code}")
        print(f"Response content: {response.text}")
        return None, None


def get_playback_state(access_token):
    ensure_wifi()  # Ensure Wi-Fi connection before making the API call
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get('https://api.spotify.com/v1/me/player', headers=headers)
    gc.collect()  # Free up memory after the request
    if response.status_code == 200:
        data = response.json()
        return data.get('is_playing', False)  # Return the actual state of is_playing
    elif response.status_code == 401:
        print("Access token expired. Refreshing token...")
        new_access_token, new_refresh_token = refresh_access_token(secrets.REFRESH_TOKEN)
        if new_access_token:
            secrets.ACCESS_TOKEN = new_access_token
            return get_playback_state(new_access_token)  # Retry getting the playback state
        else:
            print("Failed to refresh access token.")
            return False
    else:
        print(f"Failed to get playback state: {response.status_code}")
        print(f"Response content: {response.text}")
        return False

def ensure_wifi():
    """Ensure that Wi-Fi is connected, and reconnect if necessary."""
    import network
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print("Wi-Fi connection lost. Reconnecting...")
        wlan.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
        print("Reconnected to Wi-Fi")

def set_volume(access_token, volume, artist, track):
    volume = max(0, min(100, volume))  # Ensure volume is between 0 and 100
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'Content-Length': '0'
    }
    url = f'https://api.spotify.com/v1/me/player/volume?volume_percent={volume}'
    response = requests.put(url, headers=headers)
    if response.status_code == 204:
        print(f"Volume set to {volume}%")
        lcd.clear()
        lcd.putstr(f"Volume {volume}%")
        time.sleep(1.5)
        update_lcd(track, artist)
    else:
        print(f"Failed to set volume: {response.status_code}")
        print(f"Response content: {response.text}")

def toggle_play_pause(access_token, is_playing):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'Content-Length': '0'
    }
    print(is_playing)
    action = "pause" if is_playing else "play"
    response = requests.put(f'https://api.spotify.com/v1/me/player/{action}', headers=headers)
    if response.status_code == 204:
        print(f"Music {'paused' if action == 'pause' else 'playing'}")
    else:
        print(f"Failed to toggle play/pause: {response.status_code}")
        print(f"Response content: {response.text}")
    time.sleep(0.25)

def skip_track(access_token, direction):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'Content-Length': '0'
    }
    action = "next" if direction == 'next' else "previous"
    response = requests.post(f'https://api.spotify.com/v1/me/player/{action}', headers=headers)
    if response.status_code == 204:
        print(f"Skipped to {action} track")
    else:
        print(f"Failed to skip track: {response.status_code}")
        print(f"Response content: {response.text}")

def main():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
    while not wlan.isconnected():
        time.sleep(1)
    print('Connected to Wi-Fi')

    # Initial track information and playback state
    global volume, last_api_call_time, last_button_time, debounce_time, track_name, artist_name, interval, skip, lcd_track, lcd_artist
    track_name, artist_name, duration_ms, progress_ms = get_current_track(secrets.ACCESS_TOKEN)
    is_playing = get_playback_state(secrets.ACCESS_TOKEN)
    print(is_playing)
    if track_name is None:
        track_name, artist_name = "None", "None"
        duration_ms, progress_ms = 0, 0
        interval = 15  # Default to 15 seconds when no track is playing
    else:
        # Calculate interval in seconds
        interval = max(0, (duration_ms + 1000 - progress_ms) // 1000)
        update_lcd(track_name, artist_name)

    # Initialize variables for timer, button debounce, and playback state
    volume = 50  # Initial volume
    last_api_call_time = time.ticks_ms()
    last_button_time = time.ticks_ms()
    last_time = time.ticks_ms()
    current2_time = time.ticks_ms()
    skip = 0

    # Attach interrupts to buttons
    button_vol_up.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: handle_button_interrupt(PIN_VOL_UP))
    button_vol_down.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: handle_button_interrupt(PIN_VOL_DOWN))
    button_play_pause.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: handle_button_interrupt(PIN_PLAY_PAUSE))
    button_next_track.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: handle_button_interrupt(PIN_NEXT_TRACK))
    button_prev_track.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: handle_button_interrupt(PIN_PREV_TRACK))

    while True:
        # Ensure Wi-Fi is still connected
        ensure_wifi()
        
        current2_time = time.ticks_ms()
        if time.ticks_diff(current2_time, last_time) >= 15000:
            last_time = time.ticks_ms()
            is_playing = get_playback_state(secrets.ACCESS_TOKEN)
        if is_playing:
            current_time = time.ticks_ms()
            if time.ticks_diff(current_time, last_api_call_time) >= interval * 1000:  # Convert interval to ms
                track_name, artist_name, duration_ms, progress_ms = get_current_track(secrets.ACCESS_TOKEN)
                if track_name is None:
                    track_name, artist_name, duration_ms, progress_ms = "None", "None", 0, 0
                    interval = 15  # Default to 15 seconds when no track is playing
                else:
                    # Recalculate interval
                    interval = max(0, (duration_ms + 1000 - progress_ms) // 1000)
                    update_lcd(track_name, artist_name)
                last_api_call_time = current_time  # Reset the timer
            
            if len(track_name) < 16:
                track_name = format_to_lcd(track_name)
            if len(artist_name) < 16:   
                formatted_artist = format_to_lcd(artist_name)
                # Scroll if track or artist name is too long
            if (len(track_name) > 16) and (skip != 1):
                scroll_track(track_name, artist_name)
            if (len(artist_name) > 16) and (skip != 1):
                scroll_artist(track_name, artist_name)
            if lcd_artist != artist_name:
                update_artist(artist_name)
            if lcd_track != track_name:
                update_track(track_name)      
            skip = 0
        # Run garbage collection periodically
        gc.collect()
        
def scroll_track(track_name, artist_name):
    global skip
    track_length = len(track_name)
    update_artist(artist_name[0:16])
    for i in range(track_length - 15):  # +1 to ensure the last part is displayed
        if skip == 1:
            break
        substring = track_name[i:i+16]  # Get 15 character substring
        update_track(substring)
        time.sleep(1)  # Adjust the sleep time for smoother scrolling (500ms here)
    update_track(track_name[0:16])

def scroll_artist(track_name, artist_name):
    global skip
    artist_length = len(artist_name)
    update_track(track_name[0:16])
    for i in range(artist_length - 15):  # +1 to ensure the last part is displayed
        if skip == 1:
            break
        substring = artist_name[i:i+16]  # Get 15 character substring
        update_artist(substring)
        time.sleep(1)
    update_artist(artist_name[0:16])

def handle_button_interrupt(pin):
    global is_playing, volume, last_api_call_time, interval, last_button_time, track_name, artist_name, skip
    current_time = time.ticks_ms()
    print(time.ticks_diff(current_time, last_button_time))

    if pin == PIN_VOL_UP:
        volume = min(volume + 5, 100)
        set_volume(secrets.ACCESS_TOKEN, volume, artist_name, track_name)
    
    elif pin == PIN_VOL_DOWN:
        volume = max(volume - 5, 0)
        set_volume(secrets.ACCESS_TOKEN, volume, artist_name, track_name)
    
    elif pin == PIN_PLAY_PAUSE:
        is_playing = get_playback_state(secrets.ACCESS_TOKEN)
        toggle_play_pause(secrets.ACCESS_TOKEN, is_playing)
        if not is_playing:
            interval = 15  # Set interval to 15 seconds if paused

    elif pin == PIN_NEXT_TRACK:
        skip = 1
        skip_track(secrets.ACCESS_TOKEN, 'next')
        last_api_call_time = time.ticks_ms()
        track_name, artist_name, duration_ms, progress_ms = get_current_track(secrets.ACCESS_TOKEN)
        if len(track_name) < 16:
            format_to_lcd(track_name)
        if len(artist_name) < 16:
            format_to_lcd(artist_name)
        update_lcd(track_name, artist_name)
        interval = max(0, (duration_ms + 1000 - progress_ms) // 1000) if track_name else 15

    elif pin == PIN_PREV_TRACK:
        skip = 1
        skip_track(secrets.ACCESS_TOKEN, 'previous')
        track_name, artist_name, duration_ms, progress_ms = get_current_track(secrets.ACCESS_TOKEN)
        if len(track_name) < 16:
            format_to_lcd(track_name)
        if len(artist_name) < 16:
            format_to_lcd(artist_name)
        update_lcd(track_name, artist_name)
        interval = max(0, (duration_ms + 1000 - progress_ms) // 1000) if track_name else 15
        last_api_call_time = time.ticks_ms()

    last_button_time = current_time  # Update last button time for debounce


def format_to_lcd(temp):
    
    length = len(temp)
    length = 16 - length
    
    temp = temp + " "*length
    
    return temp  # Truncate and pad with spaces


# Run the main function
if __name__ == "__main__":
    main()



 