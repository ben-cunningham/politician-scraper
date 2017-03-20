class Queries:

    create_edge = """
    create table edge (
        "to" char,
        "from" char,
        "sentence" char,
        "classification" char,
        constraint edge_pk primary key ("to", "from")
    );
    """
    
    create_vertex = """
    create table vertex(
        entity char(10) primary key,
        name char(100),
        url varchar(500)
    );
    """

    insert_politician = """
    insert into vertex (entity, name, url)
    values (%s, %s, %s);
    """

    insert_connection = """
    insert into edge(to, from, cls, inf)
    values (%s, %s, %s, %s);
    """

    fetch_rows = """
    select * from vertex limit 20;
    """

    get_entity = """
    select * from vertex where name=%s;
    """
