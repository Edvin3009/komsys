from stmpy import Driver, Machine


class Quiz:
    def on_init(self):
        print("Init!")
        self.answer = ""

    def send_question(self, question):
        print("Question asked")
        self.mqtt_client.publish("quiz/question", question)

    def send_answer(self, answer):
        print("Question anwered")
        self.mqtt_client.publish("quiz/answer", answer)

    def press_buzzer(self):
        print("Buzzer pressed")
        self.mqtt_client.publish("quiz/buzzer", "Buzzer pressed")


# states

S1 = {
    "name": "S1",
}

S2 = {
    "name": "S2",
    "entry": "start_timer('buzzer_timer', 20000)"
}

S3 = {
    "name": "S3",
    "entry": "start_timer('answer_timer', 5000)"
}

# initial transition
t0 = {"source": "initial", "target": "S1"}

t1 = {
    "trigger": "message",
    "source": "S1",
    "target": "S2",
}

t2 = {
    "trigger": "buzzer_timer",
    "source": "S2",
    "target": "S3",
}

t3 = {
    "trigger": "answer_timer",
    "source": "S3",
    "target": "S1",
}

t4 = {
    "trigger": "answer",
    "source": "S3",
    "target": "S1",
}