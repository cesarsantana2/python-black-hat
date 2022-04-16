from configparser import ExtendedInterpolation
from email.message import _PayloadType
from burp import IBurpExtender
from burp import IIntruderPayloadGeneratorFactory
from burp import IIntruderPayloadGenerator

from java.util import List, ArrayList

import random

class BurpExtender(IBurpExtender, IIntruderPayloadGeneratorFactory):
    def registerExtenderCallbacks(self, callbacks):
        self.callbacks = callbacks
        self._helpers = callbacks.getHelpers()

        callbacks.registerIntruderPayloadGeneratorFactory(self)

        return

    def getGeneratorName(self):
        return "BHP Payload Generator"

    def createNewInstance(self, attack):
        return BHPFuzzer(self, attack)


class BHPFuzzer(IIntruderPayloadGenerator):
    def __init__(self, extender, attack):
        self._extender = extender
        self._helpers = extender._helpers
        self._attack = attack
        self.max_payloads = 10
        self.num_iterations = 0

        return

    def hasMorePayloads(self):
        if self.num_iterations == self.max_payloads:
            return False
        else:
            return True

    def getNextPayload(self, current_payload):

        #converte em uma string
        payload = "".join(chr(x) for x in current_payload)

        #chama o nosso modificador simples para fazer fuzzing no POST
        payload = self.mutate_payload(payload)

        #incrementa o numero de tentativas de fuzzing
        self.num_iterations += 1

        return payload

    def reset(self):
        self.num_iterations = 0
        return 


    def mutate_payload(self, original_payload):
        #escolhe um modificador simples ou pode até mesmo chamar um script exteno
        picker = random.randint(1,3)

        #seleciona um offset aleatório no payload para ser modificado 
        offset = random.randint(0, len(original_payload)-1)
        payload = original_payload[:offset]

        #insere uma tentativa de injeção de SQL no offset aleatório
        if picker == 1:
            payload += "'"
        
        #insere uma tentativa de XSS
        if picker == 2:
            payload += "<script>alert('BHP!');</script>"

        #repete uma porção do payload original uma quantidade aleatória de vezes 
        if picker == 3:

            chunk_length = random.randint(len(payload[offset:]),len(payload)-1)
            repeater = random.randint(1,10)

            for i in range(repeater):
                payload += original_payload[offset:offset+chunk_length]

        #acrescenta a parte restante do payload
        payload += original_payload[offset:]

        return payload