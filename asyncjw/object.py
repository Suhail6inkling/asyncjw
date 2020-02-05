class Object():
    
    def __eq__(self, other):
        if isinstance(other, Object):
            try:
                return self.id == other.id and self.type == other.type
            except:
                return super().__eq__(other)
        return super().__eq__(other)