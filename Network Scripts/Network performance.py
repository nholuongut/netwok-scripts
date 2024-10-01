from speedtest import Speedtest

# create a Speedtest object
st = Speedtest()

# get download and upload speeds in bits per second
download_speed = st.download()
upload_speed = st.upload()

# convert speeds to megabits per second
download_speed = download_speed / 1_000_000
upload_speed = upload_speed / 1_000_000

# print results
print(f"Download speed: {download_speed:.2f} Mbps")
print(f"Upload speed: {upload_speed:.2f} Mbps")