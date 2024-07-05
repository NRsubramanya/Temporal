from temporalio import activity

class TranslateActivities:
    def __init__(self):
        pass
    
    @activity.defn
    async def greet_in_spanish(self, name: str) -> str:
        greeting = self.generate_greeting(name)
        return greeting
    
    @activity.defn
    async def farewell_in_spanish(self, name: str) -> str:
        farewell = self.generate_farewell(name)
        return farewell



    # Method to generate greeting message
    def generate_greeting(self, name: str) -> str:
        return f"Hola, {name}!"

    # Method to generate farewell message
    def generate_farewell(self, name: str) -> str:
        return f"Adiós, {name}!"


