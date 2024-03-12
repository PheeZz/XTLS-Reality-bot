if __name__ == "__main__":
    import asyncio

    from source.database import Creator

    creator = Creator()
    asyncio.run(creator.recreate_all_tables())
