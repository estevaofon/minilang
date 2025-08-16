// Exemplo: atribuições multinível com refs (3 níveis)

struct Member
    id: int,
    next: ref Member
end

struct Team
    lead: ref Member,
    deputy: ref Member
end

struct Department
    team: ref Team
end

// Cria um departamento e monta a hierarquia multinível
print("Department example:")

let dept: ref Department = null

// Aloca Department
dept = Department(null)
print("Department created")

// Cria Team
dept.team = Team(null, null)
print("Team created")

// Atribui membros no nível 2
dept.team.lead = Member(101, null)
dept.team.deputy = Member(202, null)
print("Members assigned")

// Atribuição multinível adicional: cria o next do lead
dept.team.lead.next = Member(303, null)
print("Lead.next assigned")

// Verificações
print("Expect IDs: 101, 202, 303")
print(to_str(dept.team.lead.id))
print(to_str(dept.team.deputy.id))
print(to_str(dept.team.lead.next.id))


