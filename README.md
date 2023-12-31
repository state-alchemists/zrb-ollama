# Zrb Ollama

Zrb Ollama is a [pypi](https://pypi.org) package that acts as Ollama's wrapper, allowing you to incorporate LLM into your workflow.

## Installation

You can install Zrb Ollama by invoking the following command:

```bash
# From pypi
pip install zrb-ollama
# From github
pip install git+https://github.com/goFrendiAsgard/zrb-ollama.git@main
# From directory
pip install --use-feature=in-tree-build path/to/this/directory
```

## Installing Ollama

You can install Ollama by visiting the official website: [`https://ollama.ai/`](https://ollama.ai/).

## Talk to Zrb Ollama

Once you install Zrb Ollama, you can then run it by invoking the following command:

```bash
zrb-ollama "Why is the sky blue?"
```

<details>
<summary>See the result:</summary>

```
 The sky appears blue during the day because of the scattering of sunlight by the Earth's atmosphere. When sunlight enters the Earth's atmosphere, it is scattered in all directions by molecules such as oxygen and nitrogen. Blue light has a shorter wavelength and scatters more easily than other colors, so it is scattered more widely across the sky, making it appear blue. This phenomenon is known as Rayleigh scattering.
 Support zrb growth and development!
☕ Donate at: https://stalchmst.com/donation
🐙 Submit issues/PR at: https://github.com/state-alchemists/zrb
🐤 Follow us at: https://twitter.com/zarubastalchmst
🤖 ○ ◷ 2023-12-31 10:42:03.249 ❁  49899 → 1/3 🦙              prompt • Completed in 24.471537828445435 seconds
 The sky appears blue during the day because of the scattering of sunlight by the Earth's atmosphere. When sunlight enters the Earth's atmosphere, it is scattered in all directions by molecules such as oxygen and nitrogen. Blue light has a shorter wavelength and scatters more easily than other colors, so it is scattered more widely across the sky, making it appear blue. This phenomenon is known as Rayleigh scattering.

 The color of the sky appears blue due to a natural phenomenon called Rayleigh scattering. As sunlight reaches Earth's atmosphere, it interacts with different gases and particles in the air. Blue light has a shorter wavelength and gets scattered more easily than other colors, such as red or yellow. This scattering scatters the blue light in all directions, making the sky appear blue during a clear day. However, at sunrise and sunset, the sky can display various shades of red, orange, and pink due to the presence of dust, pollutants, and water droplets in the atmosphere that scatter longer wavelengths (red and yellow) more effectively.Support zrb growth and development!
☕ Donate at: https://stalchmst.com/donation
🐙 Submit issues/PR at: https://github.com/state-alchemists/zrb
🐤 Follow us at: https://twitter.com/zarubastalchmst
🤖 ○ ◷ 2023-12-31 10:31:39.541 ❁  45446 → 1/3 🦙              prompt • Completed in 72.80772066116333 seconds
 The color of the sky appears blue due to a natural phenomenon called Rayleigh scattering. As sunlight reaches Earth's atmosphere, it interacts with different gases and particles in the air. Blue light has a shorter wavelength and gets scattered more easily than other colors, such as red or yellow. This scattering scatters the blue light in all directions, making the sky appear blue during a clear day. However, at sunrise and sunset, the sky can display various shades of red, orange, and pink due to the presence of dust, pollutants, and water droplets in the atmosphere that scatter longer wavelengths (red and yellow) more effectively.
 The sky appears blue because of a process called scattering. When sunlight enters the Earth's atmosphere, it collides with molecules such as oxygen and nitrogen dioxide, which scatter the light in all directions. Blue light has a shorter wavelength and is scattered more easily than other colors, so it is more visible to our eyes and therefore appears blue in the sky.Support zrb growth and development!
```

</details>

Zrb Ollama will save your context history in `~/.zrb-ollama-context.json`. Thus, you can continue the conversation and retain the context

```bash
zrb-ollama "Explain in more detail"
```

<details>
<summary>See the result:</summary>

```
 Sure, I'd be happy to explain in more detail!

    When sunlight enters the Earth's atmosphere, it is scattered in all directions by molecules such as oxygen and nitrogen. Blue light has a shorter wavelength and scatters more easily than other colors, so it is scattered more widely across the sky. This means that when we look up at the sky during the day, we see a lot of blue light scattered in different directions.

    This phenomenon is known as Rayleigh scattering, named after British scientist Lord Rayleigh who discovered it in 1904. The amount and direction of scattering depends on several factors, including the wavelength of the light (which determines how much it scatters),
 the temperature of the air (which affects how much water vapor is present), and the altitude of the sun in the sky (which determines where the light has to travel through the atmosphere before reaching our eyes).

    So, when we see a blue sky during the day, we can thank Rayleigh scattering for making it appear that way.
Support zrb growth and development!
☕ Donate at: https://stalchmst.com/donation
🐙 Submit issues/PR at: https://github.com/state-alchemists/zrb
🐤 Follow us at: https://twitter.com/zarubastalchmst
🤖 ○ ◷ 2023-12-31 10:43:10.450 ❁  50315 → 1/3 🦙              prompt • Completed in 56.23700976371765 seconds
 Sure, I'd be happy to explain in more detail!

When sunlight enters the Earth's atmosphere, it is scattered in all directions by molecules such as oxygen and nitrogen. Blue light has a shorter wavelength and scatters more easily than other colors, so it is scattered more widely across the sky. This means that when we look up at the sky during the day, we see a lot of blue light scattered in different directions.

This phenomenon is known as Rayleigh scattering, named after British scientist Lord Rayleigh who discovered it in 1904. The amount and direction of scattering depends on several factors, including the wavelength of the light (which determines how much it scatters), the temperature of the air (which affects how much water vapor is present), and the altitude of the sun in the sky (which determines where the light has to travel through the atmosphere before reaching our eyes).
```

</details>


## Talk is Cheap, Show Me The Code

Zrb Ollama can help you generate and run Python code.

```bash
zrb-ollama-py "x^2 + 5x + 3 = 0, find x"
```

<details>
<summary>See the result:</summary>

```
🤖 ○ ◷ 2023-12-28 07:30:38.357 ❁  47317 → 1/3 🦙              prompt • Context file: /home/gofrendi/.zrb-ollama-context.json
🤖 ○ ◷ 2023-12-28 07:30:38.357 ❁  47317 → 1/3 🦙              prompt • Sending request...
🤖 ○ ◷ 2023-12-28 07:32:41.068 ❁  47317 → 1/3 🦙              prompt • Waiting for response...
    Here's the Python code snippet that uses the quadratic formula to find the solutions for the given equation:

    ```python
    import cmath

    # coefficients
    a = 1
    b = 5
    c = 3

    # calculate discriminant
    discriminant = (b ** 2) - (4 * a * c)

    # find two solutions
    sol1 = (-b + cmath.sqrt(discriminant)) / (2 * a) if discriminant >= 0 else None
    sol2 = (-b - cmath.sqrt(-discriminant)) / (2 * a) if discriminant >= 0 else None

    print("Solutions for x:")
    if sol1 is not None:
        print(f"x1 = {sol1.real} + {sol1.imag}j")
    if sol2 is not None:
        print(f"x2 = {sol2.real} + {sol2.imag}j")
    ```

    This code imports the `cmath` library, which provides complex number support since the quadratic formula can result in complex solutions. The coefficients are defined, and then the discriminant is calculated using the given equation's coefficients. Finally, the two solutions for x are found, and their real and imaginary parts (if applicable) are printed out. If the discriminant is negative, there are no real solutions.
🤖 ○ ◷ 2023-12-28 07:34:36.751 ❁  47317 → 1/3 🦙              prompt • Response completed
🤖 ○ ◷ 2023-12-28 07:34:36.752 ❁  47317 → 1/1 ✏️           evaluate • Waiting for evaluation...
Solutions for x:
x1 = -0.6972243622680054 + 0.0j
x2 = -2.5 + -1.8027756377319946j
Support zrb growth and development!
☕ Donate at: https://stalchmst.com/donation
🐙 Submit issues/PR at: https://github.com/state-alchemists/zrb
🐤 Follow us at: https://twitter.com/zarubastalchmst
🤖 ○ ◷ 2023-12-28 07:34:36.765 ❁  47317 → 1/1 ✏️           evaluate • Completed in 238.40946054458618 seconds
Solutions for x:
x1 = -0.6972243622680054 + 0.0j
x2 = -2.5 + -1.8027756377319946j
```
</details>


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

You can configure Zrb Ollama using a few environment variables:

- `ZRB_OLLAMA_BASE_URL`: Default Ollama base URL. If not specified, Zrb Ollama will use `http://localhost:11434`.
- `ZRB_OLLAMA_DEFAULT_MODEL`: Default Ollama model. If not specified, Zrb Ollama will use `mistral`.
- `ZRB_OLLAMA_VERBOSE_EVAL`: Whether `zrb-ollama-py` shows the evaluated source code or not. If not specified, Zrb Ollama will set this to `0`


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
