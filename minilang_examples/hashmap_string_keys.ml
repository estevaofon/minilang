// HashMap (string -> int) com encadeamento separado

struct EntryS
    key: string,
    value: int,
    next: ref EntryS
end

let CAPACITY: int = 16

// Wrapper para contornar limitação de array de refs
struct Bucket
    head: ref EntryS
end

let buckets: Bucket[16] = [Bucket(null), Bucket(null), Bucket(null), Bucket(null), Bucket(null), Bucket(null), Bucket(null), Bucket(null), Bucket(null), Bucket(null), Bucket(null), Bucket(null), Bucket(null), Bucket(null), Bucket(null), Bucket(null)]

func hash_str(s: string) -> int
    // djb2-like: h = h*33 + c
    let h: int = 5381
    let i: int = 0
    while i < strlen(s) do
        let c: int = ord(s[i])
        h = h * 33 + c
        i = i + 1
    end
    if h < 0 then
        h = 0 - h
    end
    return h % CAPACITY
end

func str_eq(a: string, b: string) -> bool
    if strlen(a) != strlen(b) then
        return false
    end
    let i: int = 0
    while i < strlen(a) do
        if ord(a[i]) != ord(b[i]) then
            return false
        end
        i = i + 1
    end
    return true
end

func put_s(key: string, value: int) -> void
    let idx: int = hash_str(key)
    if buckets[idx].head == null then
        buckets[idx].head = EntryS(key, value, null)
        return
    end
    let cur: ref EntryS = buckets[idx].head
    let prev: ref EntryS = null
    while cur != null do
        if str_eq(cur.key, key) then
            cur.value = value
            return
        end
        prev = cur
        cur = cur.next
    end
    prev.next = EntryS(key, value, null)
end

func get_s(key: string) -> int
    let idx: int = hash_str(key)
    let cur: ref EntryS = buckets[idx].head
    while cur != null do
        if str_eq(cur.key, key) then
            return cur.value
        end
        cur = cur.next
    end
    return -1
end

func remove_s(key: string) -> void
    let idx: int = hash_str(key)
    let cur: ref EntryS = buckets[idx].head
    let prev: ref EntryS = null
    while cur != null do
        if str_eq(cur.key, key) then
            if prev == null then
                buckets[idx].head = cur.next
            else
                prev.next = cur.next
            end
            return
        end
        prev = cur
        cur = cur.next
    end
end

// Demonstração
print("HashMap<string,int> demo:")
put_s("one", 1)
put_s("two", 2)
put_s("three", 3)
put_s("owne", 10)   // colisão provável
print(to_str(get_s("one")))
print(to_str(get_s("two")))
print(to_str(get_s("three")))
print(to_str(get_s("owne")))

put_s("two", 22)
print(to_str(get_s("two")))

remove_s("one")
print(to_str(get_s("one")))  // -1

// checagem colisão restante
print(to_str(get_s("owne")))


