#!/usr/bin/env python

from ws4py.client.threadedclient import WebSocketClient
import base64
import json
import ssl
import subprocess
import threading
import time
import rospy
from std_msgs.msg import String


class SpeechToTextClient(WebSocketClient):
    def __init__(self, recognized_callback):
        # Note that the documentation says another URL, this is the correct one
        self.ws_url = "wss://stream.watsonplatform.net/speech-to-text/api/v1/recognize"
        username = "7a98fb0d-8c64-4014-a70e-cf81fcfe9a03"
        password = "VaEiRcjtS5rT"
        auth_string = "%s:%s" % (username, password)
        self.base64string = base64.encodestring(auth_string).replace("\n", "")
        self.recognized_callback = recognized_callback
        self.listening = False

        try:
            WebSocketClient.__init__(self, self.ws_url,
                                     headers=[("Authorization",
                                               "Basic %s" % self.base64string)])
            self.connect()
        except Exception as e:
            print "Failed to open WebSocket."
            print e

    def opened(self):
        # Note that the audio must be of rate 16000
        # Note that inactivity_timeout -1 disables the 30s default stopping
        self.send(
            '{"action": "start", "content-type": "audio/l16;rate=16000", "interim_results": true, "timestamps": true, "inactivity_timeout":-1, "model":"es-ES_BroadbandModel"}')
        self.stream_audio_thread = threading.Thread(target=self.stream_audio)
        self.stream_audio_thread.start()

    def received_message(self, message):
        message = json.loads(str(message))
        if "state" in message:
            if message["state"] == "listening" and not self.listening:
                self.listening = True
        elif "results" in message:
            self.recognized_callback(message["results"])
        elif "error" in message:
            pass
        print "Message received: " + str(message)

    def stream_audio(self):
        while not self.listening:
            time.sleep(0.1)

        reccmd = ["arecord", "-f", "S16_LE", "-r", "16000", "-t", "raw"]
        # For CHIP
        # reccmd = ["arecord", "-D", "jack",
        #           "-f", "S16_LE",
        #           "-r", "16000",
        #           "-t", "raw"]
        p = subprocess.Popen(reccmd, stdout=subprocess.PIPE)

        while self.listening:
            data = p.stdout.read(1024)

            try:
                self.send(bytearray(data), binary=True)
            except ssl.SSLError as e:
                print "error: " + str(e)

        p.kill()

    def close(self, *args):
        self.listening = False
        self.stream_audio_thread.join()
        WebSocketClient.close(self)


class WatsonSTTPub(object):
    def __init__(self):
        self.stt_client = SpeechToTextClient(self.recognized_cb)
        self.pub = rospy.Publisher('/watsontext', String, queue_size=1)

    def recognized_cb(self, results):
        #print results
        # results looks like:
        # [{u'alternatives': [{u'timestamps': [[u'also', 22.66, 22.94], [u'help', 23.11, 23.41]], u'transcript': u'also help '}], u'final': False}]
        # [{u'alternatives': [{u'timestamps': [[u'also', 22.66, 22.94], [u'help', 23.11, 23.41]], u'confidence': 0.292, u'transcript': u'also help '}], u'final': True}]
        sentence = results[0]["alternatives"][0]["transcript"]
        estado_f = results[0]["final"]
	if estado_f:
       		self.pub.publish(String(sentence))
        	print '\n    Heard:   "' + str(sentence) + '"\n'
		time.sleep(1)

    def __del__(self):
        self.stt_client.close()


if __name__ == '__main__':
    rospy.init_node('watson')
    wsttp = WatsonSTTPub()
    rospy.spin()
