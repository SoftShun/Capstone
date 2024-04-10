# 카메라 설정

import cv2  # openCV 선언

def main() :  
  camera = cv2.VidioCapture(-1) # 카메라를 비디오 입력으로 사용. -1은 카메라의 기본설정을 따른다
  camera.set(3,640) # 가로 640px
  camera.set(4,480) # 세로 480px 
  
  while (camera.isOpened()) : # 카메라가 동작하면 while 문구 실행
    _, image = camera.read()  # 카메라 프레임 값을 읽어 image에 넣음. 제대로 읽으면 True
    # image = cv2.flip(image, -1) # 카메라 180도 뒤집어줌
    cv2.imshow( ' camera test ', image) # image 파일 보여줌
    
    if cv2.waitKey(1) == ord('q') : # q 값 입력하면 종료
      break
    
  cv2.destroyALLWindows() # 모든 openCV창을 종료
  
if __name__ == '__main__' :
  main()