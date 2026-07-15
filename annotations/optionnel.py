from typing import Optional , TypedDict

def nice_message( name : Optional[str]) -> None:
    if name is None:
        print("Hello , random guy !!")
    else :
        print (f"hello , {name} !!")

class Movie(TypedDict):
    title : str
    year : int

movie = Movie(title="Inception", year=2010)


      
