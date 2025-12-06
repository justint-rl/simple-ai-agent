import ollama

def main():
  prompt = "What is the best food in nyc?"
  response = ollama.generate(model="llama3", prompt=prompt)
  print(response.get("response", ""))

if __name__ == "__main__":
  main()
