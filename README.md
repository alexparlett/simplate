# Simplate

A simple, naive, templating library.

It is simply built to take values and replace them in a template with some additional functionality around those values.

## Syntax

The control to indicate a value is templated is `{{ ... }}`

### Functions

There are a number of built-in functions

#### var

Supports accessing variables in the context

`{{ var(foo) }}`

`{{ var(foo.bar) }}`

#### default

Similar to var but supports n number of arguments with the last argument being the default literal

`{{ default(foo, bar, dog, cat) }} => cat`

#### map

Map a value in the context, treating it as an iterator and returns a list of the mapped values. Works best in conjunction with pipe.

i.e. a context of `foo: [bar,cat]`

`{{ map(foo, Hello {{ var(this) }}) }} => [Hello bar, Hello cat]`

#### pipe

Pipe a number of functions together, passing the result of the previous to the next

e.g.

`{{ pipe( var(foo) | uppercase()) }}`

#### join

joins together the current context, built to work with pipe

#### uppercase

uppercases the current context, built to work with pipe

#### lowercase

lowercases the current context, built to work with pipe
