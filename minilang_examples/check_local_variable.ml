let a: int = 10
print(to_str(a))

func teste(a: int) -> void
    a = 20
    print(to_str(a))
    a = 30
    print(to_str(a))
    let b: int = 50
    print(to_str(b))
    b = 60
    print(to_str(b))
end

teste(a)
print(to_str(a))
let a: int = 40
print(to_str(a))
