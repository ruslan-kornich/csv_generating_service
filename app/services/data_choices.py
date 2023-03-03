SEPARATOR_CHOICES = (
    (",", "Comma(,)"),
    ("|", "Forward slash (|)"),
    (";", "Semicolon(;)"),
)

STRING_CHARACTER_CHOICES = (
    ('"', 'Double-quote(")'),
    ("'", "Single-quote(')"),
    ("'''", "Triple-quote(''')"),
    ('"""', 'Triple-quote(""")'),
    ("()", "Bracket(())"),
    ("[]", "Straight Brackets([])"),
)

TYPE_CHOICES = (
    ("full_name", "Full Name"),
    ("company", "Company"),
    ("address", "Address"),
    ("job", "Job"),
    ("email", "Email"),
    ("phone", "Phone"),
    ("text", "Text"),
    ("int", "Integer"),
    ("date", "Date"),
)
STATUS_CHOICES = (("ready", "ready"), ("process", "processing"))
