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
🤖 ○ ◷ 2023-12-28 07:52:14.327 ❁  56368 → 1/3 🦙              prompt • Context file: /home/gofrendi/.zrb-ollama-context.json
🤖 ○ ◷ 2023-12-28 07:52:14.327 ❁  56368 → 1/3 🦙              prompt • Sending request...
🤖 ○ ◷ 2023-12-28 07:52:31.962 ❁  56368 → 1/3 🦙              prompt • Waiting for response...
    The color of the sky appears blue due to a process called Rayleigh scattering. When sunlight, which is made up of different colors, enters Earth's atmosphere, it interacts with various gases and particles in the air. Blue light has a shorter wavelength and gets scattered more easily than other colors, such as red or yellow. As a result, when we look up at the sky, we predominantly see the blue light that has been scattered, making the sky appear blue to our eyes.
🤖 ○ ◷ 2023-12-28 07:53:02.411 ❁  56368 → 1/3 🦙              prompt • Response completed
Support zrb growth and development!
☕ Donate at: https://stalchmst.com/donation
🐙 Submit issues/PR at: https://github.com/state-alchemists/zrb
🐤 Follow us at: https://twitter.com/zarubastalchmst
🤖 ○ ◷ 2023-12-28 07:53:02.417 ❁  56368 → 1/3 🦙              prompt • Completed in 48.08835458755493 seconds
 The color of the sky appears blue due to a process called Rayleigh scattering. When sunlight, which is made up of different colors, enters Earth's atmosphere, it interacts with various gases and particles in the air. Blue light has a shorter wavelength and gets scattered more easily than other colors, such as red or yellow. As a result, when we look up at the sky, we predominantly see the blue light that has been scattered, making the sky appear blue to our eyes.
```

</details>

Zrb Ollama will save your context history in `~/.zrb-ollama-context.json`. Thus, you can continue the conversation and retain the context

```bash
zrb-ollama "Explain in more detail"
```

<details>
<summary>See the result:</summary>

```
🤖 ○ ◷ 2023-12-28 07:56:06.981 ❁  58272 → 1/3 🦙              prompt • Context file: /home/gofrendi/.zrb-ollama-context.json
🤖 ○ ◷ 2023-12-28 07:56:06.982 ❁  58272 → 1/3 🦙              prompt • Sending request...
🤖 ○ ◷ 2023-12-28 07:56:32.304 ❁  58272 → 1/3 🦙              prompt • Waiting for response...
    Certainly! The color of the sky is an intriguing optical phenomenon that results from the scattering of sunlight in Earth's atmosphere. To provide a more detailed explanation, let's delve into the physics behind it.

    First, it's important to understand that sunlight is composed of various colors, each with its own distinct wavelength. The electromagnetic spectrum includes radio waves, microwaves, infrared radiation, visible light, ultraviolet radiation, and X-rays. Visible light, which we can see, comprises approximately 400 to 780 nanometers (nm) in wavelength. Blue light has a shorter wavelength, typically between 450 and 495 nm.

    As sunlight enters Earth's atmosphere, it interacts with various gases and particles, such as nitrogen (N2), oxygen (O2), water vapor (H2O), and dust particles. These molecules and particles scatter the sunlight in all directions due to their size and the particular wavelengths of light they interact with most strongly. This phenomenon is called scattering.

    Now comes the interesting part: Blue light gets scattered more easily than other colors, such as red or yellow, due to its shorter wavelength. Specifically, Rayleigh scattering causes the sky to appear blue. Rayleigh scattering occurs when the gas molecules in the atmosphere scatter the short-wavelength light more effectively than longer wavelengths. This is because the size of the gas molecules in the Earth's atmosphere is much smaller than the wavelength of visible light, and they interact more with shorter-wavelength blue light than longer-wavelength red or yellow light.

    As a result, when we look up at the sky, we predominantly see the blue light that has been scattered, making the sky appear blue to our eyes. It's important to note that this is not an all-encompassing explanation, as other factors can influence the color of the sky, such as pollution and the presence of other atmospheric particles. Nonetheless, the fundamental process of Rayleigh scattering explains why the sky appears blue most of the time under clear weather conditions.
🤖 ○ ◷ 2023-12-28 07:59:53.549 ❁  58272 → 1/3 🦙              prompt • Response completed
Support zrb growth and development!
☕ Donate at: https://stalchmst.com/donation
🐙 Submit issues/PR at: https://github.com/state-alchemists/zrb
🐤 Follow us at: https://twitter.com/zarubastalchmst
🤖 ○ ◷ 2023-12-28 07:59:53.550 ❁  58272 → 1/3 🦙              prompt • Completed in 226.5693118572235 seconds
 Certainly! The color of the sky is an intriguing optical phenomenon that results from the scattering of sunlight in Earth's atmosphere. To provide a more detailed explanation, let's delve into the physics behind it.

First, it's important to understand that sunlight is composed of various colors, each with its own distinct wavelength. The electromagnetic spectrum includes radio waves, microwaves, infrared radiation, visible light, ultraviolet radiation, and X-rays. Visible light, which we can see, comprises approximately 400 to 780 nanometers (nm) in wavelength. Blue light has a shorter wavelength, typically between 450 and 495 nm.

As sunlight enters Earth's atmosphere, it interacts with various gases and particles, such as nitrogen (N2), oxygen (O2), water vapor (H2O), and dust particles. These molecules and particles scatter the sunlight in all directions due to their size and the particular wavelengths of light they interact with most strongly. This phenomenon is called scattering.

Now comes the interesting part: Blue light gets scattered more easily than other colors, such as red or yellow, due to its shorter wavelength. Specifically, Rayleigh scattering causes the sky to appear blue. Rayleigh scattering occurs when the gas molecules in the atmosphere scatter the short-wavelength light more effectively than longer wavelengths. This is because the size of the gas molecules in the Earth's atmosphere is much smaller than the wavelength of visible light, and they interact more with shorter-wavelength blue light than longer-wavelength red or yellow light.

As a result, when we look up at the sky, we predominantly see the blue light that has been scattered, making the sky appear blue to our eyes. It's important to note that this is not an all-encompassing explanation, as other factors can influence the color of the sky, such as pollution and the presence of other atmospheric particles. Nonetheless, the fundamental process of Rayleigh scattering explains why the sky appears blue most of the time under clear weather conditions.
```

</details>


## Talk is Cheap, Show Me The Code

Zrb Ollama can help you generate and run Python code.

```bash
zrb-ollama-py ""x^2 + 5x + 3 = 0, find x""
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
from zrb_ollama import PromptTask

chat = PromptTask(
    name='chat',
    model='mistral',
    prompt='echo {{ " ".join(input._args) if input._args | length > 0 else "tell me some fun fact" }}',  # noqa
    options={
        'temperature': 0.8,
        'num_gpu': 0
    },
    system_prompt='You are a code tutor. You eager to explain code in a very detail manner',  # noqa
    context_file='.ctx.json'
)
runner.register(chat)
```

```
zrb chat "Please explain the following Python script: $(cat fibo.py)"
zrb chat "Can you make it better?"
```

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
