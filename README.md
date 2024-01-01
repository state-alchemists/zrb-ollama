![](https://raw.githubusercontent.com/goFrendiAsgard/zrb-ollama/main/_images/android-chrome-192x192.png)

# Zrb Ollama

Zrb Ollama is a [pypi](https://pypi.org) package that acts as Ollama and LangChain wrapper, allowing you to incorporate LLM into your workflow.

# Installation

You can install Zrb Ollama by invoking any of the following commands:

```bash
# From pypi
pip install zrb-ollama
# From github
pip install git+https://github.com/goFrendiAsgard/zrb-ollama.git@main
# From directory
pip install --use-feature=in-tree-build path/to/this/directory
```

## Installing Ollama

By default, Zrb Ollama uses Ollama-based LLM. You can install Ollama by visiting the official website: [`https://ollama.ai/`](https://ollama.ai/).

You can change this behavior by setting `OPENAI_API_KEY`.

# Configuration

You can configure Zrb Ollama using a few environment variables:

- `OPENAI_API_KEY`: If set, Zrb-ollama will use OpenAI instead of Ollama.
- `ZRB_OLLAMA_BASE_URL`: Default Ollama base URL. If not specified, Zrb Ollama will use `http://localhost:11434`.
- `ZRB_OLLAMA_DEFAULT_MODEL`: Default Ollama model. If not specified, Zrb Ollama will use `mistral`.

# Talk to Zrb Ollama

Zrb Ollama provides a simple CLI command to interact with the LLM. This CLI command also manages your chat history and saves everything under `~/.zrb-ollama-context.json`.

Let's see the following example:

```bash
zrb-ollama "Why is the sky blue?"
```

<details>
<summary>👇See the output</summary>

```
The sky appears blue due to a phenomenon called Rayleigh scattering. When sunlight enters Earth's atmosphere, it encounters molecules and tiny particles in the air. The shorter wavelengths of light, such as blue and violet, are scattered more strongly by these particles compared to the longer wavelengths of light, like red and orange. As a result, the blue light gets scattered in all directions, creating the blue appearance of the sky.
```

</details>

Zrb Ollama will explain why the sky is blue.

Next, you can ask it to give a more detailed explanation:

```bash
zrb-ollama "Explain in more detailed"
```

<details>
<summary>👇See the output</summary>

```
Sure! When sunlight reaches Earth's atmosphere, it is composed of different colors of light, each with a different wavelength. The shorter wavelengths, such as blue and violet, have higher energy, while the longer wavelengths, such as red and orange, have lower energy.

As sunlight enters the atmosphere, it interacts with the molecules and tiny particles present in the air. These particles include nitrogen and oxygen molecules, as well as dust, water droplets, and other small particles.

The interaction between the sunlight and these particles causes a scattering of light. This scattering process is known as Rayleigh scattering. It is named after the British physicist Lord Rayleigh, who first explained it in the 19th century.

Rayleigh scattering occurs when the size of the particles in the atmosphere is much smaller than the wavelength of light. In this case, the scattering is inversely proportional to the fourth power of the wavelength. This means that shorter wavelengths, such as blue and violet light, are scattered much more strongly than longer wavelengths, such as red and orange light.

As a result, when sunlight enters the atmosphere, the blue and violet light is scattered in all directions by the particles in the air. This scattered blue light then reaches our eyes from all parts of the sky, making it appear blue to us.

It's important to note that the scattering of light is not limited to just the blue color. However, since our eyes are more sensitive to blue light, we perceive the scattered blue light more prominently, hence the blue appearance of the sky.

At sunrise or sunset, when the sun is lower in the sky, the sunlight has to pass through a larger portion of the atmosphere before reaching us. This longer path causes more scattering and absorption of shorter wavelengths, like blue and violet light, resulting in the red, orange, and pink hues commonly seen during these times.

In summary, the sky appears blue due to Rayleigh scattering, where the shorter wavelengths of sunlight, particularly blue and violet light, are scattered more strongly by the particles in the atmosphere, making the scattered blue light dominant in our perception.
```

</details>

It will understand that you asked for a more detailed explanation of why the sky is blue.

# Talk is Cheap, Show Me The Code

Furthermore, Zrb Ollama also allows you to use an AI Agent. This AI Agent can access the internet and interact with the Python interpreter.

Zrb Ollama Agent will show you the reasoning process, the solution, and the respecting Python code.

Note that for this to work, you need better LLM models like `Mistral` or Open AI.

Let's see the following example:

```bash
# You can use Ollama's mistral model:
# export ZRB_OLLAMA_DEFAULT_MODEL=mistral

# or you can use Open AI:
export OPENAI_API_KEY=your-api-key

zrb-ollama-agent "What is the area of a square with 20 cm perimeter?"
```

<details>
<summary>👇See the output</summary>

```
Thought: To find the area of a square, we need to know the side length. We can calculate the side length by dividing the perimeter by 4. Once we have the side length, we can use the formula for the area of a square, which is side length squared.

    Action: Python code

    ```python
    # Calculating the area of a square
    perimeter = 20
    side_length = perimeter / 4
    area = side_length ** 2
    # Displaying the solution
    print(area)
    ```
    I need to provide the input for the action, which is the value of the perimeter.

    Action: python_repl
    Action Input: 20
    The code executed successfully and provided the expected output.

    Final Answer:
    - Solution: The area of a square with a perimeter of 20 cm is 25 square centimeters.
    - Code:
      ```python
      # Calculating the area of a square
      perimeter = 20
      side_length = perimeter / 4
      area = side_length ** 2
      # Displaying the solution
      print(area)
      ```
```

</details>

# Getting Creative

The Zrb Ollama CLI program is helpful on its own. You can, for example, ask the LLM model to explain a code for you and refactor it.

```bash
zrb-ollama "What this code do? $(cat fibo.py)"
zrb-ollama "Can you make it better?"
```

There are a lot of things you can do with Zrb Ollama.

# Creating Custom PromptTasks

Finally, you can incorporate Zrb Ollama into your [Zrb](https://pypi.org/project/zrb) project workflow. Zrb Ollama introduce a `PromptTask` class that you can use to create more customized LLM tasks.

## Creating a PromptTask

You can also import `zrb-ollama` into your Zrb project and perform some fun things:

```python
from zrb import runner
from zrb_ollama import PromptTask, ollama_chat_model_factory

chat = PromptTask(
    name='chat',
    prompt='echo {{ " ".join(input._args) if input._args | length > 0 else "tell me some fun fact" }}',  # noqa
    system_prompt='You are a code tutor. You eager to explain code in a very detail manner',  # noqa
    chat_model_factory=ollama_chat_model_factory(
        model='mistral',
        temperature=0.8,
        num_gpu=0,
    ),
    history_file='.ctx.json'
)
runner.register(chat)
```

```bash
zrb chat "Please explain the following Python script: $(cat fibo.py)"
```

<details>
<summary>See the result:</summary>

```
🤖 ○ ◷ 2023-12-28 18:11:54.418 ❁  32106 → 1/3 🐻            zrb chat • Context file: .ctx.json
🤖 ○ ◷ 2023-12-28 18:11:54.418 ❁  32106 → 1/3 🐻            zrb chat • Sending request...
🤖 ○ ◷ 2023-12-28 18:24:32.398 ❁  32106 → 1/3 🐻            zrb chat • Waiting for response...
    Sure thing! This code defines a Python function named `fibo` that calculates the Fibonacci sequence up to the nth number. Here's a step-by-step breakdown of how it works:

    1. The function definition begins with `def fibo(n):`, which means we are defining a function named `fibo` that takes one argument, `n`.
    2. The first line inside the function is an if statement: `if n <= 1:` This statement checks if the value of `n` is less than or equal to 1. If it is, then the condition is true and we execute the code inside the indented block.
    3. Inside the if block, we return the value `1`. This is the base case for our Fibonacci sequence. The first number in the sequence (indexed at 0) is always 0, and the second number (indexed at 1) is always 1. Since our function accepts an argument of `n` instead of `n-1`, we set the base case to be when `n` is less than or equal to 1, which corresponds to the first two numbers in the sequence.
    4. If the condition in the if statement is false (i.e., if `n > 1`), then we execute the code outside of the if block. The first line here is a recursive call to `fibo(n-1)`. This means that we are calling the `fibo` function with an argument one less than our original `n`, which corresponds to the previous number in the sequence.
    5. The second recursive call inside the function is `fibo(n-2)`, which calculates the next number before that in the sequence.
    6. Finally, we return the sum of the results from the two most recent calls to `fibo`: `return fibo(n-1) + fibo(n-2)`. This is how we calculate the nth number in the Fibonacci sequence by adding together the previous two numbers.
    7. The last lines of the code are an if statement that checks if the script is being run directly (`if __name__ == '__main__'`), and if so, it prints out the result of calling `fibo(8)`. This allows us to test the function with a specific input value.
🤖 ○ ◷ 2023-12-28 18:27:42.230 ❁  32106 → 1/3 🐻            zrb chat • Response completed
Support zrb growth and development!
☕ Donate at: https://stalchmst.com/donation
🐙 Submit issues/PR at: https://github.com/state-alchemists/zrb
🐤 Follow us at: https://twitter.com/zarubastalchmst
🤖 ○ ◷ 2023-12-28 18:27:42.245 ❁  32106 → 1/3 🐻            zrb chat • Completed in 947.8267965316772 seconds
To run again: zrb chat "Explain this code: def fibo(n):
    if n <= 1:
        return 1
    return fibo(n-1) + fibo(n-2)


if __name__ == '__main__':
    print(fibo(8))"
```

</details>

```bash
zrb chat "Can you make it better?"
```

<details>
<summary>See the result:</summary>

```
🤖 ○ ◷ 2023-12-28 18:29:37.978 ❁  39864 → 1/3 🍐            zrb chat • Context file: .ctx.json
🤖 ○ ◷ 2023-12-28 18:29:37.978 ❁  39864 → 1/3 🍐            zrb chat • Sending request...
🤖 ○ ◷ 2023-12-28 18:32:21.021 ❁  39864 → 1/3 🍐            zrb chat • Waiting for response...
    Certainly! The current implementation of the `fibo` function using recursion is a common and effective way to calculate Fibonacci numbers, but it can be memory intensive for large inputs due to the repeated calculation of intermediate results. A more space-efficient alternative is to use an iterative approach instead.

    Here's an example of how you could modify the `fibo` function to use iteration:

    ```python
    def fibo(n):
        if n <= 0:
            return "Input should be positive integer"
        elif n == 1:
            return 1
        else:
            a, b = 1, 1
            for _ in range(n - 1):
                a, b = b, a + b
            return b

    if __name__ == '__main__':
        print(fibo(8))
    ```

    In this version of the function:

    1. We still start by checking for edge cases, including `n <= 0`, which returns an error message and is not part of the Fibonacci sequence. We also check if `n == 1`, which is our base case and sets the initial value of our sequence to 1.                                                                            2. For larger values of `n`, we use a pair of variables, `a` and `b`, initialized to 1 in this example, to represent the previous two numbers in the Fibonacci sequence. We then enter a for loop that runs `n-1` times.                                                                                                  3. In each iteration of the loop, we update the values of `a` and `b` by swapping their values (`a, b = b, a + b`) and moving the new value of `b` one step forward in the sequence. This allows us to calculate each number in the sequence without having to store all previous results in memory.
    4. Finally, we return the value of `b`, which is now the nth number in the Fibonacci sequence.

    Using an iterative approach can be more space-efficient than recursion for large inputs, as it avoids the need to maintain a growing call stack. However, the choice between recursion and iteration ultimately depends on the specific use case and performance requirements of your application.
🤖 ○ ◷ 2023-12-28 18:36:05.722 ❁  39864 → 1/3 🍐            zrb chat • Response completed
Support zrb growth and development!
☕ Donate at: https://stalchmst.com/donation
🐙 Submit issues/PR at: https://github.com/state-alchemists/zrb
🐤 Follow us at: https://twitter.com/zarubastalchmst
🤖 ○ ◷ 2023-12-28 18:36:05.723 ❁  39864 → 1/3 🍐            zrb chat • Completed in 387.7480981349945 seconds    
To run again: zrb chat "Can you make it better?"
```

</details>


# Configuration

# For maintainers

## Publish to pypi

To publish zrb-ollama, you need to have a `Pypi` account:

- Log in or register to [https://pypi.org/](https://pypi.org/)
- Create an API token

You can also create a `TestPypi` account:

- Log in or register to [https://test.pypi.org/](https://test.pypi.org/)
- Create an API token

Once you have your API token, you need to create a `~/.pypirc` file:

```
[distutils]
index-servers =
   pypi
   testpypi

[pypi]
  repository = https://upload.pypi.org/legacy/
  username = __token__
  password = pypi-xxx-xxx
[testpypi]
  repository = https://test.pypi.org/legacy/
  username = __token__
  password = pypi-xxx-xxx
```

To publish zrb-ollama, you can do the following command:

```bash
zrb plugin publish
```

## Updating version

You can update zrb-ollama version by modifying the following section in `pyproject.toml`:

```toml
[project]
version = "0.0.2"
```

## Adding dependencies

To add zrb-ollama dependencies, you can edit the following section in `pyproject.toml`:

```toml
[project]
dependencies = [
    "Jinja2==3.1.2",
    "jsons==1.6.3"
]
```

## Adding script

To make zrb-package-name executable, you can edit the following section in `pyproject.toml`:

```toml
[project-scripts]
zrb-ollama = "zrb-ollama.__main__:hello"
```

This will look for `hello` callable inside of your `__main__.py` file
