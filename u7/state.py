from stmpy import Driver, Machine


class Quiz:
    def on_init(self, mqtt_client, driver):
        print("Init!")
        self.mqtt_client = mqtt_client
        self.first_buzzer = None
        self.driver = driver

    def send_question(self, e):
        print("Question asked! Timer started for 20 seconds")
        self.mqtt_client.publish("quiz/question", "Press the buzzer before 20 seconds if you know the answer!")

    def answer_received(self, e):
        if e.data.get('participant') == self.first_buzzer:
            print(f"{self.first_buzzer} answered {e.data.get('answer')}")

    def buzzer_press(self, e):
        print("Buzzer pressed")
        if self.first_buzzer == None:
            self.first_buzzer = e.data.get('participant', 'Unknown')
            print(f"First buzzer was {self.first_buzzer}")
            self.mqtt_client.publish("quiz/question", f"participant {self.first_buzzer} gets to answer")

    def reset(self, e):
        self.first_buzzer = None
        self.mqtt_client.publish("quiz/question", "Waiting for next question")

    def on_timeout(self, e):
        if self.first_buzzer == None:
            print("Buzzer timeout")
            self.mqtt_client.publish("quiz/buzzer", "No one pressed the buzzer in time")
        else:
            print("Answer timeout")
            self.mqtt_client.publish("quiz/question", f"{self.first_buzzer} did not answer in time")
        
    


# states

S1 = {
    "name": "S1",
}

S2 = {
    "name": "S2",
    "entry": "start_timer('buzzer_timer', 20000)",
}

S3 = {
    "name": "S3",
}

# initial transition
t0 = {"source": "initial", "target": "S1"}

t1 = {
    "trigger": "message",
    "source": "S1",
    "target": "S2",
    "effect": "send_question; start_timer('answer_timer', 5000)"
}

t2 = {
    "trigger": "buzzer_timer",
    "source": "S2",
    "target": "S1",
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
    "effect": "answer_received"
}