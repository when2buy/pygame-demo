import sys
import random

import pygame


# 初始化Pygame
pygame.init()

# 设置窗口大小
WIDTH, HEIGHT = 768, 512
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("pygame demo")

background = pygame.image.load("./res/image/bg.png")

# 加载墙壁图像
wall_image = pygame.image.load("./res/image/wall-stone.png")
wall_image = pygame.transform.scale(wall_image, (16, 16))  # 将墙壁图像缩放为16x16

# 加载门的图像
door_image = pygame.image.load("./res/image/door.png")
door_image = pygame.transform.scale(door_image, (16, 16))

# 定义房间颜色
FLOOR_COLOR = (240, 240, 240)

# 定义绘制墙壁的函数
def draw_wall(surface, x, y, width, height):
    for i in range(0, width, 16):
        for j in range(0, height, 16):
            surface.blit(wall_image, (x + i, y + j))

walls = [
    pygame.Rect(*pos)
    for pos in [
        (0, 0, 768, 16),      # 上墙
        (0, 0, 16, 512),       # 左墙
        (768-16, 0, 16, 768),  # 右墙
        (0, 512-16, 768, 16),  # 下墙
        (512-16, 0, 16, 512),
        (0, 128, 256-16, 16),
        (256+16, 128, 256-32, 16),
        (128+32, 128+32, 16, 256-48),
        (128+32, 128+256, 16, 256),
        (128-32, 128+16, 16, 128-32),
        (128, 256, 16, 128-16),
        (256+128, 128+16, 16, 128-32),
        (256+128-48, 256, 16, 128-16),
        (256+128-48, 256+128+32, 16, 128-16),
        (16, 256, 128, 16),
        (16, 256+128-32, 128-32, 16),
        (256-32, 128+48, 128-16, 16),
        (256+128-48, 256, 128+32, 16),
        (256+128-48, 256+128, 128+32, 16),
        (128+32, 256+128, 64+32, 16),
        (256-16, 256+128+32, 64+32, 16),
        (128, 256+128+48, 32, 16),
    ]
]

# 定义墙和门的矩形列表
doors = [
    pygame.Rect(*pos)
    for pos in [
        (256-16, 128, 16, 16),
        (256, 128, 16, 16),
        (128+32, 128+256-16, 16, 16),
        (256+128-48, 256+128-16, 16, 16),
        (256+128-48, 256+128+16, 16, 16),
    ]  
]

# 修改碰撞检测函数
def get_collision_point(human_rect):
    """获取角色的碰撞检测点（底部中心点）"""
    return (human_rect.centerx, human_rect.bottom - 8)  # 底部向上8像素的中心点

# 修改can_move_to_position函数
def can_move_to_position(surface, point):
    try:
        color = surface.get_at(point)
        return not is_dark_grey(color)
    except:
        return False

# 修改获取随机有效位置的函数
def get_random_valid_position(walls, doors, human_size):
    while True:
        x = random.randint(human_size[0], 496 - human_size[0])
        y = random.randint(human_size[1], 496 - human_size[1])
        human_rect = pygame.Rect(x, y, human_size[0], human_size[1])
        collision_point = get_collision_point(human_rect)
        
        # 检查碰撞
        can_move = True
        
        # 检查墙壁碰撞
        for wall in walls:
            if wall.collidepoint(collision_point):
                can_move = False
                break
                
        # 检查门碰撞
        for door in doors:
            if door.collidepoint(collision_point):
                can_move = False
                break
                
        if can_move:
            return x, y

# 加载猴子图像
HUMAN_SPRITES = {
    'left': [],
    'right': [],
    'up': [],
    'down': []
}

for direction in ['left', 'right', 'up', 'down']:
    for i in range(4):  # 假设每个方向有4帧动画
        img = pygame.image.load(f"./res/image/boy1.png")
        HUMAN_SPRITES[direction].append(pygame.transform.scale(img, (16, 32)))

# 在主循环中添加
current_frame = 0
animation_speed = 0.2
last_direction = 'right'

# 在主循环前添加以下函数
def is_dark_grey(color):
    # 定义深灰色的阈值，可以根据需要调整
    threshold = 100
    return all(c < threshold for c in color[:3])

# 初始化两个角色的位置
boy_rect = pygame.Rect(0, 0, 16, 32)
girl_rect = pygame.Rect(0, 0, 16, 32)

# 确保两个角色不会重叠
while True:
    boy_rect.x, boy_rect.y = get_random_valid_position(walls, doors, (16, 32))
    girl_rect.x, girl_rect.y = get_random_valid_position(walls, doors, (16, 32))
    
    # 检查两个角色是否重叠
    if not boy_rect.colliderect(girl_rect):
        break

# 移动速度和方向控制
HUMAN_SPEED = 4
move_direction = {'left': False, 'right': False, 'up': False, 'down': False}
HUMAN_COLLISION_SHRINK = 8  # 减小碰撞检测范围，让移动更畅

# 加载角色图像
boy_sprites = {
    'left': [],
    'right': [],
    'up': [],
    'down': []
}

girl_sprites = {
    'left': [],
    'right': [],
    'up': [],
    'down': []
}

# 加载两个角色的精灵图
for direction in ['left', 'right', 'up', 'down']:
    for i in range(4):
        boy_img = pygame.image.load(f"./res/image/boy1.png")
        girl_img = pygame.image.load(f"./res/image/girl1.png")
        boy_sprites[direction].append(pygame.transform.scale(boy_img, (16, 32)))
        girl_sprites[direction].append(pygame.transform.scale(girl_img, (16, 32)))

# 创建切换按钮
BUTTON_WIDTH = 256-16
BUTTON_HEIGHT = 64
button_rect = pygame.Rect(512, 16, BUTTON_WIDTH, BUTTON_HEIGHT)
button_color = (100, 100, 255)
button_hover_color = (150, 150, 255)
font = pygame.font.Font(None, 24)

# 添加角色状态变量
current_character = 'boy'  # 或 'girl'
HUMAN_SPRITES = boy_sprites  # 默认使用男孩精灵
current_frame = 0
animation_speed = 0.2

# 在初始化部分，修改角色的初始位置设置
# 为两个角色分别创建矩形和状态
boy_rect = pygame.Rect(0, 0, 16, 32)
girl_rect = pygame.Rect(0, 0, 16, 32)
boy_rect.x, boy_rect.y = get_random_valid_position(walls, doors, (16, 32))
girl_rect.x, girl_rect.y = get_random_valid_position(walls, doors, (16, 32))

# 为两个角色分别创建移动状态和方向
boy_move_direction = {'left': False, 'right': False, 'up': False, 'down': False}
girl_move_direction = {'left': False, 'right': False, 'up': False, 'down': False}
boy_last_direction = 'right'
girl_last_direction = 'right'

# 主循环
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_a:
                if current_character == 'boy':
                    boy_move_direction['left'] = True
                else:
                    girl_move_direction['left'] = True
            elif event.key == pygame.K_d:
                if current_character == 'boy':
                    boy_move_direction['right'] = True
                else:
                    girl_move_direction['right'] = True
            elif event.key == pygame.K_w:
                if current_character == 'boy':
                    boy_move_direction['up'] = True
                else:
                    girl_move_direction['up'] = True
            elif event.key == pygame.K_s:
                if current_character == 'boy':
                    boy_move_direction['down'] = True
                else:
                    girl_move_direction['down'] = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                if current_character == 'boy':
                    boy_move_direction['left'] = False
                else:
                    girl_move_direction['left'] = False
            elif event.key == pygame.K_d:
                if current_character == 'boy':
                    boy_move_direction['right'] = False
                else:
                    girl_move_direction['right'] = False
            elif event.key == pygame.K_w:
                if current_character == 'boy':
                    boy_move_direction['up'] = False
                else:
                    girl_move_direction['up'] = False
            elif event.key == pygame.K_s:
                if current_character == 'boy':
                    boy_move_direction['down'] = False
                else:
                    girl_move_direction['down'] = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_pos):
                # 切换角色
                if current_character == 'boy':
                    current_character = 'girl'
                    HUMAN_SPRITES = girl_sprites
                else:
                    current_character = 'boy'
                    HUMAN_SPRITES = boy_sprites

    # 更新男孩位置
    new_boy_rect = boy_rect.copy()
    if boy_move_direction['left']:
        new_boy_rect.x -= HUMAN_SPEED
        boy_last_direction = 'left'
    if boy_move_direction['right']:
        new_boy_rect.x += HUMAN_SPEED
        boy_last_direction = 'right'
    if boy_move_direction['up']:
        new_boy_rect.y -= HUMAN_SPEED
        boy_last_direction = 'up'
    if boy_move_direction['down']:
        new_boy_rect.y += HUMAN_SPEED
        boy_last_direction = 'down'

    # 更新女孩位置
    new_girl_rect = girl_rect.copy()
    if girl_move_direction['left']:
        new_girl_rect.x -= HUMAN_SPEED
        girl_last_direction = 'left'
    if girl_move_direction['right']:
        new_girl_rect.x += HUMAN_SPEED
        girl_last_direction = 'right'
    if girl_move_direction['up']:
        new_girl_rect.y -= HUMAN_SPEED
        girl_last_direction = 'up'
    if girl_move_direction['down']:
        new_girl_rect.y += HUMAN_SPEED
        girl_last_direction = 'down'

    # 检查碰撞并更新位置
    for new_rect, rect in [(new_boy_rect, boy_rect), (new_girl_rect, girl_rect)]:
        collision_point = get_collision_point(new_rect)
        can_move = True
        
        # 检查墙壁碰撞
        for wall in walls:
            if wall.collidepoint(collision_point):
                can_move = False
                break
        
        # 如果碰到门则允许移动
        for door in doors:
            if door.collidepoint(collision_point):
                can_move = True
                break
            
        # 检查背景碰撞
        if can_move and can_move_to_position(background, collision_point):
            rect.x, rect.y = new_rect.x, new_rect.y

    # 确保角色不会移出屏幕
    boy_rect.clamp_ip(screen.get_rect())
    girl_rect.clamp_ip(screen.get_rect())

    # 绘制背景
    screen.fill(FLOOR_COLOR)
    screen.blit(background, (0, 0))

    # 绘制墙壁和门
    for wall in walls:
        draw_wall(screen, wall.x, wall.y, wall.width, wall.height)
    
    for door in doors:
        screen.blit(door_image, door)

    # 绘制两个角色
    if any(boy_move_direction.values()) or any(girl_move_direction.values()):
        current_frame = (current_frame + animation_speed) % 4

    # 绘制男孩
    screen.blit(boy_sprites[boy_last_direction][int(current_frame)], boy_rect)
    # 绘制女孩
    screen.blit(girl_sprites[girl_last_direction][int(current_frame)], girl_rect)

    # 当前控制的角色绘制一个简单的标记（比如一个小圆圈）
    current_rect = boy_rect if current_character == 'boy' else girl_rect
    pygame.draw.circle(screen, (255, 0, 0), 
                      (current_rect.centerx, current_rect.top - 5), 3)

    # 绘制切换按钮
    mouse_pos = pygame.mouse.get_pos()
    button_current_color = button_hover_color if button_rect.collidepoint(mouse_pos) else button_color
    pygame.draw.rect(screen, button_current_color, button_rect)
    pygame.draw.rect(screen, (50, 50, 200), button_rect, 2)  # 按钮边框
    
    # 增大字体大小
    button_text = pygame.font.Font(None, 36).render("change role", True, (255, 255, 255))
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)

    # # 在绘制两个角色后添加以下代码
    # # 可视化碰撞点
    # boy_collision = get_collision_point(boy_rect)
    # girl_collision = get_collision_point(girl_rect)
    
    # # 绘制角色完整区域（黄色框）
    # pygame.draw.rect(screen, (255, 255, 0), boy_rect, 1)  # 男孩完整区域
    # pygame.draw.rect(screen, (255, 255, 0), girl_rect, 1)  # 女孩完整区域

    # # 绘制碰撞点（红色点）
    # pygame.draw.circle(screen, (255, 0, 0), boy_collision, 2)  # 男孩碰撞点
    # pygame.draw.circle(screen, (255, 0, 0), girl_collision, 2)  # 女孩碰撞点

    # 更新显示
    pygame.display.flip()

    # 控制帧率
    clock.tick(60)

# 退出Pygame
pygame.quit()
sys.exit()
