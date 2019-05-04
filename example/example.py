import requests

def pushStack(str): 
    targetUrl = "https://stack-string.herokuapp.com/PushStack?string=" + str
    requests.post(targetUrl)


def popStack():
    r = requests.get("https://stack-string.herokuapp.com/PopStack")
    print(r.text)


if __name__ == "__main__":
    pushStack("testStr")
    popStack()
