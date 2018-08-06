import glob
import cv2
import os


def main():

    # 캐스케이드 파일의 경로 지정하기
    cascade_file = "./opencv/data/haarcascades/haarcascade_frontalface_default.xml"
    # 얼굴 인식 전용 캐스케이드 파일 읽어 들이기
    cascade = cv2.CascadeClassifier(cascade_file)

    # 폴더 이름을 리스트로 받음
    file_path = './resources/images/gender/'
    dirs = os.listdir(file_path)
    for idx, dir in enumerate(dirs, 0):
        # input path
        image_file = file_path + dir + '/*'
        if not os.path.isdir(file_path + str(idx) + '_' + dir):
            # create output dir
            os.mkdir(file_path + str(idx) + '_' + dir)
        # output path
        output_path = file_path + str(idx) + '_' + dir + '/'

        # 폴더안의 모든 이미지파일을 rgb로 읽고(1) 리스트로 담는다
        images = [cv2.imread(file, 1) for file in glob.glob(image_file)]

        cnt = 0
        for image in images:
            # 얼굴 인식 실행하기
            # detectMultiScale - 얼굴 인식. minSize 이하의 크기는 무시. 너무 작게 지정하면 배경 등을 얼굴로 잘못 인식하게 된다.
            face_list = cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=1, minSize=(85, 85))
            if len(face_list) == 1: # 여러명 인식된 사진 거르기
                for face in face_list:
                    x, y, w, h = face
                    # 이미지 trim
                    trimed_img = image[y:y + h, x:x + w]
                    # 이미지 resize (80 x 80)
                    resized_img = cv2.resize(trimed_img, (80, 80))
                    # 이미지를 저장
                    cv2.imwrite(output_path + str(cnt) + '.jpg', resized_img)

                    print('success')
            else:
                print("no face")

            cnt += 1


if __name__ == '__main__':
    print('start....')
    main()
    print('end....')
