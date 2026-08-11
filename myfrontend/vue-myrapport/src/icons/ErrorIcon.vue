<template>
    <svg
        class="w-10 h-10 text-white icon"
        viewBox="0 0 52 52"
        fill="none"
    >
        <circle class="circle" cx="26" cy="26" r="24"/>
        <path class="cross1" d="M18 18L34 34"/>
        <path class="cross2" d="M34 18L18 34"/>
    </svg>
</template>

<style scoped>
    .icon{
    animation:shake .45s ease;
    }

    circle,path{
        stroke:currentColor;
        stroke-width:3;
        stroke-linecap:round;
    }

    .circle{
        stroke-dasharray:166;
        stroke-dashoffset:166;
        animation:draw .45s forwards;
    }

    .cross1{
        stroke-dasharray:23;
        stroke-dashoffset:23;
        animation:draw .25s .35s forwards;
    }

    .cross2{
        stroke-dasharray:23;
        stroke-dashoffset:23;
        animation:draw .25s .55s forwards;
    }

    @keyframes draw{
        to{
        stroke-dashoffset:0;
        }
    }

    @keyframes shake{
        25%{transform:translateX(-3px)}
        50%{transform:translateX(3px)}
        75%{transform:translateX(-2px)}
        100%{transform:none}
    }
</style>