from app_factory import create_app
import config


if __name__ == '__main__':
    app = create_app(config_object=config)
    
    app.run('0.0.0.0')