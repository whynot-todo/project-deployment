window.onload = function () {
    const btn = document.getElementById("btn")
    const inputEle = document.getElementById("score")
    const rankEle = document.getElementById("rank")
    const diffEle = document.getElementById("diff")
    const diffDayEle = document.getElementById("diff-days")
    const processEle = document.getElementById("process")
    const diffProcess = document.getElementById("diff-process")
    const skillNumEle = document.getElementById("skill-num")
    const diffYearsEle = document.getElementById("diff-years")
    const calcTimeEle = document.getElementById("calc-time")
    const skillPointsEve = 80


    const getLevelArr = () => {
        const result = []
        start_pre = 0
        end_pre = 0
        for (let i = 1; i <= 100; i++) {
            result.push({
                level: i,
                start: start_pre + (i - 1) * skillPointsEve,
                end: end_pre + i * skillPointsEve
            })

            start_pre = start_pre + (i - 1) * skillPointsEve
            end_pre = end_pre + i * skillPointsEve
        }
        return result
    }

    const getLevel = (levelArr, value) => {
        const resultObj = levelArr.find(_i => _i.start <= value & _i.end > value)
        return resultObj ? resultObj : {
            level: 0,
            start: 0,
            end: 0
        }
    }

    const processProgress = (current, total) => {
        const precent = current / total
        const wrapperWidth = window.getComputedStyle(processEle).width
        const innerWidth = wrapperWidth.slice(0, -2) * 1 * precent
        diffProcess.style.width = `${innerWidth}px`
    }

    const setViewNum = (obj,levelArr) => {
        const { currentVal, start, end, level,calcTime} = obj
        const diff = end - currentVal
        const used = currentVal - start
        const total = end - start
        rankEle.innerText = level
        diffEle.innerText = diff
        diffDayEle.innerText = (diff / skillPointsEve).toFixed(2)
        skillNumEle.innerText = `${used} / ${total}`
        diffYearsEle.innerText = `${(levelArr[levelArr.length - 1].end - currentVal) / skillPointsEve}`
        calcTimeEle.innerText = calcTime
        processProgress(used, total)

    }
    const getCache = () => {
        const objStr = window.localStorage.getItem("calcObj")
        return JSON.parse(objStr)
    }

    const setCache = (obj) => {
        const _str = JSON.stringify(obj)
        window.localStorage.setItem("calcObj", _str)
    }

    let levelArr = null;
    const init = () => {
        levelArr = getLevelArr()
        const data = getCache()
        if (data) {
            setViewNum(data,levelArr)
            inputEle.value = data.currentVal
        }
    }

    init()

    btn.onclick = () => {
        const inputVal = inputEle.value * 1
        if (!inputVal) return
        const { level, start, end } = getLevel(levelArr, inputVal)
        const date = new Date()
        const calcTime = `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()} ${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`
        const calcObj = {currentVal:inputVal,start,end,level,calcTime}
        setViewNum(calcObj,levelArr)
        setCache(calcObj)
    }

}

