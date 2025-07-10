# users/management/commands/load_characters.py

import os
import uuid
from django.core.management.base import BaseCommand
from django.conf import settings
from users.models import Character  # 'users'는 앱 이름에 맞게!

class Command(BaseCommand):  # ✅ 꼭 이 이름이어야 함!
    help = 'static/characters 폴더에 있는 이미지 파일로 Character 모델 자동 생성'

    def handle(self, *args, **kwargs):
        # static/characters 폴더 경로
        static_dir = os.path.join(settings.BASE_DIR, 'static', 'images','characters')

        # 예쁜 이름 매핑 (필요시 추가)
        pretty_names = {
            "cat": "마동석냥이",
            "forest_keeper": "행복한 숲지기",
            "ginseng": "행복을 나누는 인삼",
            "happy_beginner": "행복한 뉴비",
            "kind_golem": "친절한 골렘",
            "magician": "츤데레 숲마법사",
            "running_person": "뛰어다니는 사람",
            "shark": "서있는 상어",
            "stone": "그냥 돌맹이",
 
        }


        for filename in os.listdir(static_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                name_key = os.path.splitext(filename)[0]
                name = pretty_names.get(name_key, name_key)
                image_url = f"characters/{filename}"

                if Character.objects.filter(image_url=image_url).exists():
                    self.stdout.write(self.style.WARNING(f"⚠️ {image_url} 이미 있음. 스킵"))
                    continue

                Character.objects.create(
                    character_id=uuid.uuid4(),
                    name=name,
                    image_url=image_url
                )
                self.stdout.write(self.style.SUCCESS(f"✅ 생성됨: {name} - {image_url}"))
