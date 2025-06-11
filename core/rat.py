class RegisterAliasTable:
    def __init__(self, num_registers=32):
        # Cada registrador tem: tag (ou None) e validade (True=valor pronto, False=aguardando)
        self.table = {f'R{i}': {'tag': None, 'valid': True} for i in range(num_registers)}

    def set_alias(self, reg, tag):
        # Associa um registrador a um novo tag (ex: ao despachar para o ROB) e marca como inválido.
        if reg in self.table:
            self.table[reg]['tag'] = tag
            self.table[reg]['valid'] = False

    def set_valid(self, reg):
        # Marca o registrador como válido (valor pronto).
        if reg in self.table:
            self.table[reg]['valid'] = True

    def clear_alias(self, reg, tag):
        # Limpa o alias se o tag for igual (usado no commit).
        if reg in self.table and self.table[reg]['tag'] == tag:
            self.table[reg]['tag'] = None
            self.table[reg]['valid'] = True

    def get_tag(self, reg):
        # Retorna o tag associado ao registrador (ou None).
        return self.table.get(reg, {}).get('tag', None)

    def is_valid(self, reg):
        # Retorna True se o valor do registrador está pronto.
        return self.table.get(reg, {}).get('valid', True)

    def __repr__(self):
        return str(self.table)
