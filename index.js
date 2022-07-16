window.onload = function () {
    const btn = document.getElementById("btn")
    const inputEle = document.getElementById("score")
    const rankEle = document.getElementById("rank")
    const diffEle = document.getElementById("diff")

    const level = [
        { level: 1, start: 0, end: 100 }
    ]

    const getLevelArr = () => {
        const result = []
        start_pre = 0
        end_pre = 0
        for (let i = 1; i <= 100; i++) {
            result.push({
                level: i,
                start: start_pre + (i - 1) * 30,
                end: end_pre + i * 30
            })

            start_pre = start_pre + (i - 1) * 30
            end_pre = end_pre + i * 30
        }
        return result
    }

    const getLevel = (levelArr, value) => {
        const resultObj = levelArr.find(_i => _i.start <= value & _i.end > value)
        const deffValue = resultObj ? (resultObj.end - value) : 0
        const level = resultObj ? resultObj.level : 0
        return [level, deffValue]
    }

    btn.onclick = () => {
        const inputVal = inputEle.value * 1
        if (!inputVal) return
        const levelArr = getLevelArr()
        const [level, diff] = getLevel(levelArr, inputVal)
        rankEle.innerText = level
        diffEle.innerText = diff
    }

}

