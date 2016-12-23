class Queries:

    create_edge = """
    create table edge (
        "to" int,
        "from" int
    );
    """
    
    create_vertex = """
    create table vertex(
        name char(100)
    );
    """
