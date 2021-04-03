import CommunicationManager as CM
import MachineLearningManager as ML
import threading
import time
import sys

# [Aufgabe3] Parameter für OPC UA Verbindung aus dem Script auslesen und hier eintragen
# [Aufgabe3] Bei der URL an das OPC-Prefix denken und den Port mit anhängen
# [Aufgabe3] NodeIDs auffüllen
OpcuaURL = "opc.tcp://127.0.0.1:4840"
nodeIdsListUeb = [
    'ns=3;s="DB_OPC_UA"."IMS_5A_M0009682"."I_Eingaenge"."I_IMS5A_IL"',
    'ns=3;s="DB_OPC_UA"."IMS_5A_M0009682"."I_Eingaenge"."I_IMS5A_B4"']

# [Aufgabe3] Parameter für MQTT Verbindung aus dem Script auslesen und hier eintragen
# [Aufgabe3] Es wird höchst wahrscheinlich mit Werkstückträger 001 gearbeitet. Sollte dies nicht der Fall sein,
# [Aufgabe3] wird der Übungsleiter bekanntgeben, welcher Werkstückträger verwendet wird.
MqttUrl = "127.0.0.1"
MqttPort = 1883
MqttTimeout = 60
MqttTopics = ["esp32mag"]
WSTID = "001"

#[Aufgabe4] Instanz von MachineLearningManager erstellen
MachineLM = ML.MachineLearning()

#[Aufgabe3] Instanz von CommunicationManager erstellen
CommunicationM = CM.CommunicationManager(swtid = WSTID)

#Prediction Thread
__startPredicitingThread = None


# [Aufgabe3] Zuerst den aktuellen Snapshot mit Hilfe des erstellten Communicationmanagers erfassen
# [Aufgabe3] Anschließend Array mit den Features für die Analyse Modelle erstellen.
# [Aufgabe3] Dieses Array mit Informationen aus dem Snapshot füllen.
# [Aufgabe3] Beispiel für Feature-Array (Parameter sind beispielhaft und nicht korrekt):
# [Aufgabe3] features = [snapshot[0], snapshot[2], snapshot[5]]
#snapshot =
#feature_array = [snapshot[0], snapshot[2], snapshot[5]]
#ML.MachineLearning()
# [Aufgabe4] Model mit Hilfe des erstellten ML-Managers für Vorhersagen nutzen und Antworten auswerten

# [Aufgabe4] Es gibt 3 mögliche Predictions:
# [Aufgabe4] "0" -> Fehler
# [Aufgabe4] "1" -> Kein Fehler
# [Aufgabe4] "2" -> Keine Aussage möglich
# [Aufgabe5] Erstellten Communicationmanager nutzen, um Vorhersagen nur dann auszuführen, wenn der Werkstückträger unter Station 5a ist.
# [Aufgabe5] Nach Verlassen des Werkstückträgers soll die Warnlampe weiterhin das richtige Signal anzeigen
def __PredictErrors():
    # Thread-Erstellung für Prediction-Loop. Keine Änderung am Gerüst notwendig
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        snapshot = CommunicationM.getDataSnapshot()
        features = [snapshot[0], snapshot[1], snapshot[2]]
        pred = MachineLM.predictStift(features)
        print(pred)
        handleResults(pred)
        #TODO Implementierung

		# 0.5 Sekunden Pause für eine zyklische Vorhersage im 500ms Takt zu ermöglichen. Keine Änderung nötig
        time.sleep(0.5)


# Prediction Thread Erstellung, der nach dem Start die von Ihnen angelegte Methode __PredictErrors ausführt.
# Keine Änderung nötig!
__startPredicitingThread = threading.Thread(target=__PredictErrors, args=(), name="StartPredicting")


#[Aufgabe4] Methode implementieren, die je nach Prediction die richtigen Warnlampen ansteuert
#[Aufgabe4] Die zu verwendenden IDs sind Tisch-spezifisch. Das XX in DB_OPC_Meldesignale_XX muss mit der Tischnummer ersetzt werden
#[Aufgabe4] Sobald alles funktioniert, melden Sie sich bei dem Übungsleiter, um Zugriff auf die richtigen Warnlampen zu bekommen
def handleResults(predictionStift):
    if(predictionStift == [1]):
        CommunicationM.writeStation('ns=3;s="DB_OPC_Meldesignale_13"."IMS_5A_Meldungen"."LampeRot"', False)
        CommunicationM.writeStation('ns=3;s="DB_OPC_Meldesignale_13"."IMS_5A_Meldungen"."LampeGelb"', False)
        CommunicationM.writeStation('ns=3;s="DB_OPC_Meldesignale_13"."IMS_5A_Meldungen"."LampeGruen"', True)
    elif(predictionStift== [0]):
        CommunicationM.writeStation('ns=3;s="DB_OPC_Meldesignale_13"."IMS_5A_Meldungen"."LampeRot"', True)
        CommunicationM.writeStation('ns=3;s="DB_OPC_Meldesignale_13"."IMS_5A_Meldungen"."LampeGelb"', False)
        CommunicationM.writeStation('ns=3;s="DB_OPC_Meldesignale_13"."IMS_5A_Meldungen"."LampeGruen"', False)

    elif(predictionStift== [2]):
        CommunicationM.writeStation('ns=3;s="DB_OPC_Meldesignale_13"."IMS_5A_Meldungen"."LampeRot"', False)
        CommunicationM.writeStation('ns=3;s="DB_OPC_Meldesignale_13"."IMS_5A_Meldungen"."LampeGelb"', True)
        CommunicationM.writeStation('ns=3;s="DB_OPC_Meldesignale_13"."IMS_5A_Meldungen"."LampeGruen"', False)

        # TODO Implementierung
        #Beispiel für OPC UA Write, um Warnlampe anzusprechen:
		#communicationmanager.writeStation('ns=3;s="DB_OPC_Meldesignale_13"."IMS_1_Meldungen"."LampeGelb"',False)
        #...
    #elif(predictionStift == [0]):
	#...
	#...
	#...




# [Aufgabe3] Erstellen Sie die OPC UA und MQTT Clients und starten Sie die subscriptions mit Hilfe des erstellen commuicationmanagers

# [Aufgabe3] Der MQTT Client muss nach der Erstellung und dem Anlegen der Subscription manuell mit MQTT_startClient() gestartet werden
# [Aufgabe3] Nachdem beide Clients laufen, starten Sie die Datenerfassung mit Hilfe des erstellten communicationmanagers
# [Aufgabe4] Präparieren oder trainieren Sie ein Analysemodell mit Hilfe des erstellten communicationmanagers.
# [Aufgabe4] Nutzen Sie am besten die Methode prepareModels des managers. Es sind keine Parameter notwendig
# [Aufgabe4] Nach der Referenzierung auf den globalen Thread (vorgegeben) muss dieser gestartet werden
def startProgram():
    #TODO Implementierung
    global __startPredicitingThread
    # TODO Implementierung
    CommunicationM.MQTT_CreateClient(url = MqttUrl, port = MqttPort, timeout =MqttTimeout)
    CommunicationM.MQTT_subscribeToTopic(topics=MqttTopics)
    CommunicationM.MQTT_startClient()

    CommunicationM.OPCUA_createClient(url=OpcuaURL)
    CommunicationM.OPCUA_subscribe(nodeList=nodeIdsListUeb)
    CommunicationM.startCollectingData()
    MachineLM.prepareModels()
    __startPredicitingThread.start()


def endProgram():
    sys.exit(0)

# [Aufgabe4] Methode implementieren, die alle Warnlampen unter Station 5A ausschaltet
def turnOffLights():
    pass

# [Aufgabe4] Methode implementieren, die Lampe unter Station 5A auf Grün schaltet
def LightsGreen():
    pass


# Definitionsabschnitt beendet
# Ausführung startet ab hier

print("Program Running")
print("Sie haben folgende Optionen:")
print("0 : Programm beenden")
print("1 : Programm starten")
print("2 : Lichter unter 5A ausschalten")
print("3 : Licht unter 5A auf Grün setzen")
__Run = True

while __Run == True:
    try:
        inputValue = input()
        # [Aufgabe3] OPC UA und MQTT Datenerfassung mit Hilfe des Connectionmanagers beenden (endofProgramm)
        # [Aufgabe4] Thread beenden (do_run auf false und anschließend join-Aufruf) -> Dieser Aufruf muss vor dem Beenden der Datenerfassung getätigt werden
        # [Aufgabe3/4] Dieses Programm beenden (Aus der While-Schleife springen)
        if inputValue == "0":
            CommunicationM.stopCollectionData()
            CommunicationM.OPCUA_stopClient()
            CommunicationM.MQTT_stopClient()

        # [Aufgabe3] Programmfunktionalität starten
        elif inputValue == "1":
            startProgram()


                # [Aufgabe4] Alle Lichter an Station 5A ausschalten
        elif inputValue == "2":
            turnOffLights()
            #TODO Implementierung

        # [Aufgabe4] Licht an Station 5A auf Grün schalten
        elif inputValue == "3":
            LightsGreen()
            # TODO Implementierung

        else:
            print('Bitte eine Zahl zwischen 0 und 3 eingeben!')
    except ValueError as e:
        print('ValueError:', 'Bitte eine Zahl eingeben!')
