from fixpointtool.content.fpt_content import AccessDictionaries


def plusOne(x):
    for i in range(len(x)):
        x[i] += 1


if __name__ == '__main__':

    a = AccessDictionaries()

    print(list(a.getDictionaryWithoutTransformation("mappings").keys()))