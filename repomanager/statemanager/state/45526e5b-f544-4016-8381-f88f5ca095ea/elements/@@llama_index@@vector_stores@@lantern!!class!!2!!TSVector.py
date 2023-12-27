    class TSVector(TypeDecorator):
        impl = TSVECTOR
        cache_ok = cache_okay
