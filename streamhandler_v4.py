import json
import sys

import requests
import time
import subprocess
import threading
from propertymanager import PropertyManager
from util import Util


class StreamHandler:

    def __init__(self):
        self.property_manager = PropertyManager()

    # query the discovery service to get the channel data
    def send_discovery_request(self, channelId):
        data = {"url": self.property_manager.get_channel_url() + str(channelId),
                "adapterName": "bsx3"}
        headers = {"Content-Type": "application/json"}
        response = requests.get(url=self.property_manager.get_discovery_service_url(),
                                headers=headers, json=data)
        dict = response.json()
        print(dict)
        if 'status' in dict and dict["status"] == "NULL_LINK_RETURNED":
            return "ERROR"
        return dict["link"]


    def concat_files(self, audioFilepath, mediaFilepath, outputFilepath):
        # Start ffmpeg process
        print("[INFO] Concatenating files....")
        print("[DEBUG] Audio : " + audioFilepath)
        print("[DEBUG] Media : " + mediaFilepath)
        print("[DEBUG] Output : " + outputFilepath)

        ffmpeg_path = self.property_manager.get_ffmpeg_path()
        command = [ffmpeg_path + "\\ffmpeg.exe", "-i", audioFilepath, "-i", mediaFilepath, "-c", "copy", outputFilepath]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        #
        # # Check if the process exited successfully
        # if process.returncode != 0:
        #     print(f"ffmpeg concat process failed with return code {process.returncode}")
        # else:
        #     print("ffmpeg concat process completed successfully")

    def get_stream_link(self, url : str, foldername : str,  filename : str):
        # Start ffmpeg process
        ffmpeg_path = self.property_manager.get_ffmpeg_path()
        command = [ffmpeg_path + "\\ffmpeg.exe", "-i", url, "-t", "00:09:00", foldername + "/" + filename]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

        # Read and print output in real-time
        for output_line in process.stdout:
            print(output_line, end="")

            # Check for the specific error message
            if "HTTP error 403 Forbidden" in output_line:
                print("Detected HTTP error 403 Forbidden. Terminating ffmpeg process.")
                process.terminate()
                break

        # Wait for the process to finish
        process.wait()

        # Check if the process exited successfully
        if process.returncode != 0:
            print(f"ffmpeg process failed with return code {process.returncode}")
        else:
            print("ffmpeg process completed successfully")



    def get_channel_data(self, apiUrl: str, user: str):
        channelId = 0
        response = requests.get(apiUrl)
        j = response.text
        data = json.loads(j)
        channeldata = (data['payload']['channelData'])
        for channel in channeldata.values():
            if channel['channelGroup'] == 'at home girls':
                if channel['title'] == user:
                    channelId = channel['id']
                    break
        return channelId

    def execute(self, username : str):
        print("[INFO] Running in looping mode")
        incremented_number = 0
        while True:
            channelId = self.get_channel_data( self.property_manager.get_channel_lookup_url(), username)
            if channelId == 0:
                print("[ERROR] No channel can be identified for user")
                print("[INFO] Attempting to try again in 5 minutes")
                time.sleep(300)
            else:
                print("[INFO] Channel for user is : " + str(channelId))
                link = self.send_discovery_request(channelId)
                if link != "ERROR":
                    # -- removed : incremented_number = (incremented_number +
                    username_folder = self.property_manager.get_library_path() + "/" + username
                    Util.create(username_folder + "/audio")
                    Util.create(username_folder + "/video")
                    incremented_number = Util.get_latest_counter_for_stream_file(username_folder + "/video", username)
                    # self.get_stream_link(link, username_folder, username + "_" + str(incremented_number) + ".mkv")
                    mediaThread = threading.Thread(target=self.get_stream_link, args=(link, username_folder + "/video", username + "_" + str(incremented_number) + ".mkv"))
                    audioThread = threading.Thread(target=self.get_stream_link, args=(link.replace("_vo", "_ao"), username_folder + "/audio", username + "_" + str(incremented_number) + ".mp3"))

                    mediaThread.start()
                    audioThread.start()

                    mediaThread.join()
                    audioThread.join()

                    # here, run the code to combine the audio and media
                    audioFilepath = (username_folder + "/audio/" + username + "_" + str(incremented_number) + ".mp3")
                    mediaFilepath = (username_folder + "/video/" + username + "_" + str(incremented_number) + ".mkv")
                    outputFilepath = (username_folder + "/" + username + "_" + str(incremented_number) + ".mkv")
                    self.concat_files(audioFilepath, mediaFilepath, outputFilepath)


                else:
                    print("[ERROR] Error in processing the stream. Retry in 5 minutes")
                    time.sleep(300)



if len(sys.argv) == 2:
    username = sys.argv[1]
    print("Running process for username : " + username)
    stream_handler = StreamHandler()
    stream_handler.execute(username)
else:
    print("[ERROR]. Please enter a username")
