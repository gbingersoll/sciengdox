---
title: Example Document
author: [Author]
...

# Code Listings

```{#lst:simple_listing2 .ruby caption="Listing of Ruby code"}
# A simple class
class Hello
  def go
    puts "Hello World"
  end
end
```

```{#lst:simple_listing3 .python .noexec caption="Listing of Python code that is just printed"}
# A simple class
class Hello:
    def go(__self__):
        print("Hello World")
```

# Code Execution

Defining this code block will echo the code block itself to the document and
also will execute it, printing the output to the document as well.

```{.python .echo}
class Greeter:
    def speak(__self__):
        print("Hello World")

    def respond(__self__, name):
        print(f"Hello {name}")

greeter = Greeter()
greeter.speak()
```

This next code block continues from the previous one, so variables stay defined.

```{.python .echo}
greeter.respond("Joe")
```
