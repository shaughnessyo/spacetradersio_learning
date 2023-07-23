from sqlalchemy.orm import sessionmaker



engine = sa.create_engine('postgresql://postgres:lasers@localhost:5432/spacetraders')








s.close()


# book = Book(
#     title='Deep Learning',
#     author='Ian Goodfellow',
#     pages=775,
#     published=datetime(2016, 11, 18)
# )
