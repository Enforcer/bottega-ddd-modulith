from lagom import Container, Singleton

from used_stuff_market.shared_kernel.money import Money

container = Container()


class Foo:
    def __init__(self, value: int = 5):
        self.value = value

    def __repr__(self) -> str:
        return super().__repr__() + f" {self.value=}"


class ClassNeedingFoo:
    def __init__(self, foo: Foo) -> None:
        self.foo = foo


print("\nAutodiscovery of dependencies")
instance = container[ClassNeedingFoo]  # built automagically
print(instance)
print(instance.foo)

print("\nBy default, each class is instantiated every time")
instance_2 = container.resolve(ClassNeedingFoo)
print(instance_2)  # different instance than in 1st case
print(instance_2.foo)  # ditto, Foo instance was also recreated

print("\nWe can make a dependency Singleton, that will make it created only once on the first use")
container[Foo] = Singleton(Foo)  # Make Foo a Singleton, alternative syntax: container[
instance_3 = container.resolve(ClassNeedingFoo)
print(instance_3.foo)
instance_4 = container.resolve(ClassNeedingFoo)
print(instance_4.foo)

# Alternative syntax of Singleton - can you spot the difference?
# container[Foo] = Foo()  # commented, because lagom does not allow to change existing definitions


# Need to clone the container to make changes to existing definitions
container_2 = container.clone()

print("\nOne can also use any callable as a definition")
container_2[Foo] = lambda: Foo(123)
instance_5 = container_2.resolve(ClassNeedingFoo)
print(instance_5.foo)
