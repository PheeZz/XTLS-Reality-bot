if __name__ == "__main__":
    from source.database import Creator
    import asyncio

    creator = Creator()
    asyncio.run(creator.recreate_all_tables())
