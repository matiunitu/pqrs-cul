import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), 'app'))
from controllers.usuarios_controller import UsuariosController

def main():
    controller = UsuariosController()
    from_id = 20  # usuario problemático
    to_id = 17    # destino por defecto (nelson)
    print('Reasignando PQRS de', from_id, 'a', to_id)
    res = controller.reasignar_pqrs(from_id, to_id, delete_source=True)
    print('Resultado:', res)

if __name__ == '__main__':
    main()
