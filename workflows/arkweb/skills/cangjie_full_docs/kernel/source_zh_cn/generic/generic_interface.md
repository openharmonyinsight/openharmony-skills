# 泛型接口

泛型可以用来定义泛型接口，以标准库中定义的 `Iterable` 为例，它的成员函数 `iterator` 需要返回一个 `Iterator` 类型，这一类型是一个容器的遍历器。 `Iterator` 是一个泛型接口，`Iterator` 内部有一个从容器类型中返回下一个元素的 `next` 成员函数，`next` 成员函数返回的类型是一个需要在使用时指定的类型，所以 `Iterator` 需要声明泛型参数。

<!-- compile -->

```cangjie
public interface Iterable<E> {
    func iterator(): Iterator<E>
}

public interface Iterator<E> <: Iterable<E> {
    func next(): Option<E>
}

public interface Collection<T> <: Iterable<T> {
     prop size: Int64
     func isEmpty(): Bool
}
```
